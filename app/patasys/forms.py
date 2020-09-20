from flask_wtf import FlaskForm
from datetime import datetime, timezone
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Patient, Doctor

import re


class AddPatientForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    second_name = StringField('Фамилия', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[DataRequired()])
    phone_number = StringField('Номер телефона')
    age = StringField('Vozrast')
    doctors = QuerySelectField(label='Doctor', query_factory=lambda: Doctor.query.all(), blank_text='Bez vracha', allow_blank=True)
    submit = SubmitField('Добавить пациента')


    def validate_phone_number(self, phone_number):
        number = phone_number.data
        patient = Patient.query.filter_by(phone_number=number).first()
        if patient is not None:
            raise ValidationError('Данный номер телефона привязян к другому пациенту.')
        tpl = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
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
        tpl = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
        if re.match(tpl, number) is None:
            raise ValidationError('Номер введен не верно')


class AddServiceForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    cost = StringField('Цена', validators=[DataRequired()])
    code = StringField('Код', validators=[DataRequired()])
    submit = SubmitField('Добавить услугу')


class AddVisitForm(FlaskForm):
    visit_time = StringField('Время сеанса', default=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),  validators=[DataRequired()])
    submit = SubmitField('Записать')
    