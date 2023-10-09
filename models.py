from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_card_number = db.Column(db.String(255))

    # Fields for Matric Marksheet
    matric_student_name = db.Column(db.String(255))
    matric_father_name = db.Column(db.String(255))
    matric_board_name = db.Column(db.String(255))
    matric_dob = db.Column(db.String(10))  # You can use a suitable data type for Date of Birth
    matric_obtain_marks = db.Column(db.Integer)
    matric_total_marks = db.Column(db.Integer)

    # Fields for Fsc Marksheet
    fsc_board_name = db.Column(db.String(255))
    fsc_total_marks = db.Column(db.Integer)
    fsc_obtain_marks = db.Column(db.Integer)
