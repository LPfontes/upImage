import os
import uuid
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings
from .forms import ImagemForm, ImagemFormIA
import cv2

# Define the directory where upscaled images will be saved.
OUTPUT_DIR = os.path.join(settings.MEDIA_ROOT, 'upscaled')
# Define the directory where pre-trained models are located.
MODEL_DIR = os.path.join(settings.MODEL_ROOT)
# Ensure the output directory exists; create it if it doesn't.
os.makedirs(OUTPUT_DIR, exist_ok=True)

def upScale(image, scale, interpolation):
    """
    Upscales an image using traditional interpolation methods from OpenCV.

    Args:
        image: The input OpenCV image object.
        scale (int): The scaling factor (2, 3, or 4).
        interpolation (str): The interpolation method ('Lanczos', 'Linear', or 'Cubic').

    Returns:
        The upscaled OpenCV image object.

    Raises:
        ValueError: If the interpolation method or scale factor is invalid.
    """
    # Map the string interpolation names to OpenCV constants.
    if interpolation == 'Lanczos':
        interpolation = cv2.INTER_LANCZOS4
    elif interpolation == 'Linear':
        interpolation = cv2.INTER_LINEAR
    elif interpolation == 'Cubic':
        interpolation = cv2.INTER_CUBIC
    else:
        raise ValueError('Invalid interpolation method.')

    # Check if the provided scale factor is supported.
    if scale not in [2, 3, 4]:
        raise ValueError('Invalid scale factor. Only 2x, 3x and 4x are supported.')

    # Resize the image using the specified interpolation method.
    resized_image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=interpolation)
    return resized_image

def upScaleDNNSuperRes(image, scale, model):
    """
    Upscales an image using Deep Neural Network (DNN) based Super Resolution models from OpenCV.

    Args:
        image: The input OpenCV image object.
        scale (int): The scaling factor.
        model (str): The name of the DNN model ('EDSR', 'FSRCNN', 'ESPCN', or 'LapSRN').

    Returns:
        The upscaled OpenCV image object.
    """
    # Map the model names to their corresponding prefixes used in the file names.
    model_map = {
        'EDSR': 'edsr',
        'FSRCNN': 'fsrcnn',
        'ESPCN': 'espcn',
        'LapSRN': 'lapsrn'
    }

    # Create a DNN super resolution object.
    dnn_superres = cv2.dnn_superres.DnnSuperResImpl_create()
    # Construct the path to the pre-trained model file.
    path = MODEL_DIR + f'/{model}_x{scale}.pb'
    # Read the pre-trained model.
    dnn_superres.readModel(path)
    # Set the model and the desired scale.
    dnn_superres.setModel(model_map[model], scale)
    # Upsample the input image using the loaded DNN model.
    result = dnn_superres.upsample(image)
    return result

def upload_image(request):
    """
    Handles the image upload and upscaling process.

    If the request method is POST, it processes the uploaded image based on the submitted form.
    It supports both traditional interpolation and DNN-based super-resolution.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Either a FileResponse containing the upscaled image as an attachment,
                      or an HttpResponse indicating an error or invalid form data.
    """
    if request.method == 'POST':
        # Determine which form was submitted ('normal' for traditional, 'AI' for DNN).
        form_type = request.POST.get('form_type')
        # Instantiate the appropriate form based on the form type.
        form = ImagemForm(request.POST, request.FILES) if form_type == 'normal' else ImagemFormIA(request.POST, request.FILES)

        output_path = None  # Initialize output_path to avoid errors in the finally block.

        if form.is_valid():
            # Get the uploaded image file from the form.
            image_file = form.cleaned_data['imagem']
            # Get the desired scaling factor from the form.
            scale = int(form.cleaned_data['scale'])
            # Get the interpolation method if the 'normal' form was used.
            interpolationString = form.cleaned_data['interpolation'] if form_type == 'normal' else None
            # Get the selected DNN model if the 'AI' form was used.
            model = form.cleaned_data['model'] if form_type == 'AI' else None

            # Extract the file extension from the original image name.
            extension = os.path.splitext(image_file.name)[1].lower()[1:]
            # Generate a unique temporary file name for the uploaded image.
            temp_name = f"{uuid.uuid4().hex}.{extension}"
            # Construct the full path to the temporary input file.
            input_path = os.path.join(OUTPUT_DIR, temp_name)

            try:
                # Save the uploaded image to a temporary file.
                with open(input_path, 'wb+') as dest:
                    for chunk in image_file.chunks():
                        dest.write(chunk)

                # Read the temporary image using OpenCV.
                image = cv2.imread(input_path)

                # Perform image upscaling based on the selected method.
                if form_type == 'normal':
                    resized_image = upScale(image, scale, interpolationString)
                    suffix = interpolationString
                else:  # form_type == 'AI'
                    resized_image = upScaleDNNSuperRes(image, scale, model)
                    suffix = model

                # Construct the output file name.
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_name = f'{base_name}_out_{suffix}.{extension}'
                # Construct the full path to the output file.
                output_path = os.path.join(OUTPUT_DIR, output_name)

                # Save the upscaled image to the output file.
                cv2.imwrite(output_path, resized_image)

                # If the output file was successfully created, prepare it for download.
                if os.path.exists(output_path):
                    response = FileResponse(open(output_path, 'rb'), content_type='image/' + extension)
                    response['Content-Disposition'] = f'attachment; filename="{output_name}"'
                    return response

                # If there was an issue generating the image, return an error response.
                return HttpResponse('Error generating image.', status=500)

            finally:
                # Clean up: remove the temporary input file.
                if os.path.exists(input_path):
                    os.remove(input_path)
                # Clean up: remove the generated output file (in case of an error during response).
                if output_path and os.path.exists(output_path):
                    os.remove(output_path)
        else:
            # If the submitted form data is invalid, return an error response.
            return HttpResponse('Invalid form data.', status=400)

    else:
        # If the request method is GET, render the image upload form.
        return render(request, 'index.html', {
            'form': ImagemForm(),
            'formAI': ImagemFormIA()
        })