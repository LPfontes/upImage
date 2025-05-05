import os
import uuid
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings
from .forms import ImagemForm
import cv2
OUTPUT_DIR = os.path.join(settings.MEDIA_ROOT, 'upscaled')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def upload_image(request):
    if request.method == 'POST':
        form = ImagemForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['imagem']
            extension = os.path.splitext(image_file.name)[1].lower()[1:]
            temp_name = f"{uuid.uuid4().hex}." + extension
            input_path = os.path.join(OUTPUT_DIR, temp_name)

            try:
                # Save original image temporarily
                with open(input_path, 'wb+') as dest:
                    for chunk in image_file.chunks():
                        dest.write(chunk)

                image = cv2.imread(input_path)
                resized_image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4)

                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_path = os.path.join(OUTPUT_DIR, f'{base_name}_out.' + extension)

                # Save resized image
                cv2.imwrite(output_path, resized_image)

                if os.path.exists(output_path):
                    with open(output_path, 'rb') as img:
                        response = FileResponse(img, content_type='image/' + extension)
                        response['Content-Disposition'] = f'attachment; filename="{base_name}_out.{extension}"'
                        return response

                return HttpResponse('Error generating image.', status=500)

            finally:
                # Delete temporary files
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
    else:
        form = ImagemForm()
        return render(request, 'index.html', {'form': form})


        
    
