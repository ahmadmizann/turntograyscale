import gradio as gr
import numpy as np
from PIL import Image
import tempfile

# Function to convert image to grayscale manually
def convert_to_grayscale(input_image):
    # Convert the input image to a numpy array
    img_array = np.array(input_image)

    # Calculate the grayscale values using the luminance formula
    gray_image = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]

    # Convert the grayscale values to an 8-bit format (0-255) and create a new image
    gray_image = gray_image.astype(np.uint8)
    
    # Save the grayscale image to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    Image.fromarray(gray_image).save(temp_file.name)

    return Image.fromarray(gray_image), temp_file.name  # Return both the image and the path to the temporary file

# Gradio Interface version
gr.Interface(
    fn=convert_to_grayscale,
    inputs=gr.Image(type="pil", label="Upload Your Image"),
    outputs=[gr.Image(type="pil", label="Grayscale Image"), gr.File(label="Download Grayscale Image")],  # Multiple outputs
    examples=[
        ["panda.jpg"],
        ["tiger.jpg"]
    ],
    allow_flagging="never"  # Disable the flag button
).launch()
