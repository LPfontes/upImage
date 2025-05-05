import os
import uuid
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings
from .forms import ImagemForm, ImagemFormIA
import cv2
OUTPUT_DIR = os.path.join(settings.MEDIA_ROOT, 'upscaled')
MODEL_DIR = os.path.join(settings.MODEL_ROOT)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def upScale(image, scale, interpolation):
    if interpolation == 'Lanczos':
        interpolation = cv2.INTER_LANCZOS4
    elif interpolation == 'Linear':
        interpolation = cv2.INTER_LINEAR
    elif interpolation == 'Cubic':
        interpolation = cv2.INTER_CUBIC
    else:
        raise ValueError('Invalid interpolation method.')

    if scale not in [2,3, 4]:
        raise ValueError('Invalid scale factor. Only 2x, 3x and 4x are supported.')

    resized_image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=interpolation)
    return resized_image

def upScaleDNNSuperRes(image, scale,model):
    model_map = {
    'EDSR': 'edsr',
    'FSRCNN': 'fsrcnn',
    'ESPCN': 'espcn',
    'LapSRN': 'lapsrn'
    }

    dnn_superres = cv2.dnn_superres.DnnSuperResImpl_create()
    path =MODEL_DIR + f'/{model}_x{scale}.pb'
    dnn_superres.readModel(path)
    dnn_superres.setModel(model_map[model], scale)
    result = dnn_superres.upsample(image)
    return result

def upload_image(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        form = ImagemForm(request.POST, request.FILES) if form_type == 'normal' else ImagemFormIA(request.POST, request.FILES)

        output_path = None  # Para evitar erro no finally

        if form.is_valid():
            image_file = form.cleaned_data['imagem']
            scale = int(form.cleaned_data['scale'])
            interpolationString = form.cleaned_data['interpolation'] if form_type == 'normal' else None
            model = form.cleaned_data['model'] if form_type == 'AI' else None

            extension = os.path.splitext(image_file.name)[1].lower()[1:]
            temp_name = f"{uuid.uuid4().hex}.{extension}"
            input_path = os.path.join(OUTPUT_DIR, temp_name)

            try:
                with open(input_path, 'wb+') as dest:
                    for chunk in image_file.chunks():
                        dest.write(chunk)

                image = cv2.imread(input_path)

                if form_type == 'normal':
                    resized_image = upScale(image, scale, interpolationString)
                    suffix = interpolationString
                else:
                    resized_image = upScaleDNNSuperRes(image, scale, model)
                    suffix = model

                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_name = f'{base_name}_out_{suffix}.{extension}'
                output_path = os.path.join(OUTPUT_DIR, output_name)

                cv2.imwrite(output_path, resized_image)

                if os.path.exists(output_path):
                    response = FileResponse(open(output_path, 'rb'), content_type='image/' + extension)
                    response['Content-Disposition'] = f'attachment; filename="{output_name}"'
                    return response

                return HttpResponse('Error generating image.', status=500)

            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)
                if output_path and os.path.exists(output_path):
                    os.remove(output_path)
        else:
            return HttpResponse('Invalid form data.', status=400)

    else:
        return render(request, 'index.html', {
            'form': ImagemForm(),
            'formAI': ImagemFormIA()
        })
