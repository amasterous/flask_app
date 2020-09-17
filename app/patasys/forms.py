from flask_wtf import FlaskForm
from sqlalchemy.orm.query import Query
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Patient, Doctor
import re


class AddPatientForm(FlaskForm):
    def get_patients():
        # patients = Patient.query.all()
        # return patients
        pass
    first_name = StringField('Имя', validators=[DataRequired()])
    second_name = StringField('Фамилия', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[DataRequired()])
    phone_number = StringField('Номер телефона')
    doctors = QuerySelectField(query_factory=lambda: Doctor.query.all())
    # doctor = SelectField('Doctor', choices = doctors, validators=[DataRequired()])
    submit = SubmitField('Добавить пациента')


    def validate_phone_number(self, phone_number):
        number = phone_number.data
        patient = Patient.query.filter_by(phone_number=number).first()
        if patient is not None:
            raise ValidationError('Данный номер телефона привязян к другому пациенту.')
        tpl = '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
        if re.match(tpl, number) is None:
            raise ValidationError('Номер введен не верно')



class AddDoctorForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    second_name = StringField('Фамилия', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[DataRequired()])
    phone_number = StringField('Номер телефона')
    submit = SubmitField('Добавить доктора')

    def validate_phone_number(self, phone_number):
        number = phone_number.data
        doctor = Doctor.query.filter_by(phone_number=number).first()
        if doctor is not None:
            raise ValidationError('Данный номер телефона привязян к другому доктору.')
        tpl = '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
        if re.match(tpl, number) is None:
            raise ValidationError('Номер введен не верно')
