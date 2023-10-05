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
            uploaded_files = request.files.getlist('images[]')

            if len(uploaded_files) > 0:
                results = []

                # Create a ThreadPoolExecutor for multithreading
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # Extract text from each uploaded image using OCR in separate threads
                    futures = [executor.submit(extractTextFromImage, file) for file in uploaded_files]

                    # Collect the results from the threads
                    for future in concurrent.futures.as_completed(futures):
                        results.append(future.result())

                return render_template("index.html", predictions=results)
            else:
                return render_template("index.html", predictions=["No images uploaded."])
        except Exception as e:
            return render_template("index.html", predictions=[str(e)])



if __name__ == '__main__':
    app.run(debug=True)
