# -*- coding: utf-8 -*- 
from app.auth.routes import login
from flask import render_template, redirect, flash, request
from flask.helpers import url_for
from flask_login import login_required
from werkzeug.utils import redirect
from app.patasys import bp
from flask_login import current_user
from app.patasys.forms import AddPatientForm, AddDoctorForm
from app.models import Patient, Doctor
from app import db


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('patasys/index.html', title='Home')


@login_required
@bp.route('/add', methods=['GET', 'POST'])
def add_patient():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))
    form = AddPatientForm()
    if form.validate_on_submit():
        patient = Patient(first_name=form.first_name.data, 
            second_name=form.second_name.data,
            phone_number=form.phone_number.data,
            patronymic=form.patronymic.data,
            medic=form.doctors.data
        )
        db.session.add(patient)
        db.session.commit()
        flash('Новый пациент добавлен')
        return redirect(url_for('patasys.index'))
    return render_template('patasys/add_patient.html', title='Add Patient', form=form)

@login_required
@bp.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))
    form = AddDoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(
            first_name=form.first_name.data, 
            second_name=form.second_name.data,
            phone_number=form.phone_number.data,
            patronymic=form.patronymic.data,
            age=form.age.data,
        
        )
        db.session.add(doctor)
        db.session.commit()
        flash('Новый доктор добавлен')
        return redirect(url_for('patasys.index'))
    return render_template('patasys/add_doctor.html', title='Add doctor', form=form)

@login_required
@bp.route('/all_patients')
def all_patients():
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    context = {
        'patients': patients,
        'doctors': doctors,
    }
    return render_template('patasys/all_patients.html', **context)


@login_required
@bp.route('/patient/<int:patient_id>')
def view_patient(patient_id):
    patient = Patient.query.filter_by(id=patient_id).first()
    doctor = Doctor.query.filter_by(id=patient.doctor_id).first()
    context = {
        'patient': patient,
        'doctor': doctor,
    }
    return render_template('patasys/view_patient.html', **context) 

