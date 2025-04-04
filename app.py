import fasthtml
import numpy as np
from PIL import Image
import os

app = fasthtml.App()

UPLOAD_FOLDER = "uploads/"
OUTPUT_FOLDER = "grayscale/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
async def home(request):
    if request.method == "POST":
        uploaded_file = request.files.get("image")
        if uploaded_file:
            image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            output_path = os.path.join(OUTPUT_FOLDER, "grayscale_" + uploaded_file.filename)

            # Save the uploaded image
            with open(image_path, "wb") as f:
                f.write(uploaded_file.read())

            # Convert to grayscale
            img = Image.open(image_path)
            img_array = np.array(img)
            gray_image = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]
            gray_image = gray_image.astype(np.uint8)

            # Save grayscale image
            Image.fromarray(gray_image).save(output_path)

            return {
                "message": "Success!",
                "gray_image_url": f"/static/{output_path}",
            }

    return fasthtml.render("index.html")

if __name__ == "__main__":
    app.run(debug=True)
