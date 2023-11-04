from datetime import datetime
from flask import Flask, render_template, request,Flask, render_template, request, redirect, url_for,flash
import pytesseract
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import io
import concurrent.futures

from models import Student

app = Flask(__name__)
app.secret_key = 'dsfsf2312323312gdsgsjdf' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/student_data'


db = SQLAlchemy(app)
def extract_text_from_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        return str(e)
 
def clean_and_format_text(extracted_text):
    # Split the text into lines
    lines = extracted_text.splitlines()
    return lines





 
 

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

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(extract_text_from_image, file) for file in uploaded_files]

                    for future in concurrent.futures.as_completed(futures):
                        results.append(future.result())

                formatted_results = [clean_and_format_text(result) for result in results]

                return render_template("index.html", predictions=formatted_results)
            else:
                return render_template("index.html", predictions=["No images uploaded."])
        except Exception as e:
            return render_template("index.html", predictions=[str(e)])



@app.route("/insert", methods=['GET', 'POST'])
def insert_data():
    if request.method == 'POST':
        id_card_number = request.form['id_card_number']
        matric_student_name = request.form['matric_student_name']
        matric_father_name = request.form['matric_father_name']
        matric_board_name = request.form['matric_board_name']
        matric_dob = request.form['matric_dob']
        matric_obtain_marks = request.form['matric_obtain_marks']
        matric_total_marks = request.form['matric_total_marks']
        fsc_board_name = request.form['fsc_board_name']
        fsc_total_marks = request.form['fsc_total_marks']
        fsc_obtain_marks = request.form['fsc_obtain_marks']
        formatted_dob = datetime.strptime(matric_dob, '%d-%m-%Y').strftime('%Y-%m-%d')

        # Create a new Student object and insert it into the database
        student = Student(
            id_card_number=id_card_number,
            matric_student_name=matric_student_name,
            matric_father_name=matric_father_name,
            matric_board_name=matric_board_name,
            matric_dob=formatted_dob,
            matric_obtain_marks=matric_obtain_marks,
            matric_total_marks=matric_total_marks,
            fsc_board_name=fsc_board_name,
            fsc_total_marks=fsc_total_marks,
            fsc_obtain_marks=fsc_obtain_marks,
         
        )

        db.session.add(student)
        db.session.commit()
        flash('Data inserted successfully', 'success') 
        return redirect(url_for('insert_data'))  # Redirect to the form page after submission

    return render_template("insert_data.html")


if __name__ == '__main__':
    app.run(debug=True)
