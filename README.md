# Image Upscaler Web Application

This web application allows users to upload an image and upscale it using either traditional image interpolation techniques or Deep Neural Network (DNN) based super-resolution models. Built with Django, it provides a user-friendly interface for enhancing the resolution of images directly in the browser.

## Features

* **Traditional Upscaling:** Offers several classic interpolation methods for image upscaling:
    * Lanczos
    * Linear
    * Cubic
* **AI-Powered Upscaling:** Integrates pre-trained DNN super-resolution models for more advanced upscaling:
    * EDSR (Enhanced Deep Residual Networks for Single Image Super-Resolution)
    * FSRCNN (Fast Super-Resolution Convolutional Neural Network)
    * ESPCN (Efficient Sub-Pixel Convolutional Network)
    * LapSRN (Laplacian Pyramid Super-Resolution Network)
* **Scale Factor Selection:** Users can choose the desired upscaling factor (2x, 3x, or 4x).
* **File Handling:** Supports uploading common image formats and downloads the upscaled image as a file.
* **Temporary File Management:** Cleans up temporary input and output files after processing.

## Prerequisites

Before running the application, ensure you have the following installed:

* **Python:** Version 3.x
* **pip:** Python package installer
* **Django:** Version 5.x (or the version specified in `requirements.txt`)
* **pillow** Version 11.x
* **OpenCV (cv2):** Python library for computer vision
* **Pre-trained Super-Resolution Models:** These are expected to be located in a directory specified by `MODEL_ROOT` in your Django settings.

## Installation

1.  **Clone the repository (if you have the code in a repository):**
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Django Settings:**
    * Ensure you have `MEDIA_ROOT` and `MODEL_ROOT` defined in your `settings.py` file.
    * `MEDIA_ROOT` should point to the directory where uploaded and processed images will be temporarily stored.
    * `MODEL_ROOT` should point to the directory containing the pre-trained `.pb` files for the DNN super-resolution models (e.g., `edsr_x2.pb`, `fsrcnn_x3.pb`, etc.).
    * Make sure these directories exist and are writable by the Django application.

5.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser (optional, but recommended for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

    Open your web browser and navigate to `http://127.0.0.1:8000/` to access the application.

## Usage

1.  Navigate to the application in your web browser.
2.  You will see two forms: one for traditional upscaling and another for AI-powered upscaling.
3.  **For Traditional Upscaling:**
    * Click the "Choose File" button to upload an image.
    * Select the desired "Scale" (2x, 3x, or 4x).
    * Choose an "Interpolation" method (Lanczos, Linear, or Cubic).
    * Click the "Upscale Image" button.
4.  **For AI-Powered Upscaling:**
    * Click the "Choose File" button to upload an image.
    * Select the desired "Scale" (the available scales depend on the chosen model).
    * Choose a "Model" (EDSR, FSRCNN, ESPCN, or LapSRN).
    * Click the "Upscale Image (AI)" button.
5.  The upscaled image will be processed and automatically downloaded to your computer.
## Contributing

Contributions to this project are welcome. Please feel free to submit pull requests or open issues for bug fixes, feature requests, or improvements.
