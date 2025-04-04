import fasthtml
import numpy as np
from PIL import Image
import os
import io

app = fasthtml.App()

@app.route("/", methods=["GET", "POST"])
async def home(request):
    if request.method == "POST":
        uploaded_file = request.files.get("image")
        if uploaded_file:
            # Read the image into memory
            img = Image.open(io.BytesIO(uploaded_file.read()))
            img_array = np.array(img)

            # Convert to grayscale
            gray_image = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]
            gray_image = gray_image.astype(np.uint8)
            gray_pil = Image.fromarray(gray_image)

            # Save to memory
            img_bytes = io.BytesIO()
            gray_pil.save(img_bytes, format="JPEG")
            img_bytes.seek(0)

            return app.response(img_bytes.read(), content_type="image/jpeg")

    return """
    <!DOCTYPE html>
    <html>
    <head><title>Image to Grayscale</title></head>
    <body>
        <h1>Convert Image to Grayscale</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()
