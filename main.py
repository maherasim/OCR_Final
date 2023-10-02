from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import io
import concurrent.futures  # Import concurrent.futures for multithreading

app = Flask(__name__)

def extractTextFromImage(uploaded_file):
    try:
        # Read the uploaded image file
        image = Image.open(uploaded_file)
        # Perform OCR on the image
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        return str(e)

# routes
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def get_output():
    if request.method == 'POST':
        try:
            # Get the uploaded image file
            uploaded_file = request.files['image']

            if uploaded_file.filename != '':
                # Create a ThreadPoolExecutor for multithreading
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # Extract text from the uploaded image using OCR in a separate thread
                    future = executor.submit(extractTextFromImage, uploaded_file)
                    result = future.result()  # Get the result from the thread

                return render_template("index.html", prediction=result)
            else:
                return render_template("index.html", prediction="No image uploaded.")
        except Exception as e:
            return render_template("index.html", prediction=str(e))

if __name__ == '__main__':
    app.run(debug=True)
