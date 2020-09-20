# -*- coding: utf-8 -*- 
from app.auth.routes import login
from flask import render_template, redirect, flash, request
from flask.helpers import url_for
from flask_login import login_required
from werkzeug.utils import redirect
from app.patasys import bp
from flask_login import current_user
from app.patasys.forms import AddPatientForm, AddDoctorForm, AddServiceForm, AddVisitForm
from app.models import Patient, Doctor, Service, Visit
from app import db
from datetime import datetime
import time


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('patasys/index.html', title='Home')

@bp.app_template_filter('ctime')
def timectime(s):
    value = datetime.fromtimestamp(int(s))
    return value.strftime('%Y-%m-%d %H:%M:%S')


@login_required
@bp.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))
    form = AddPatientForm()
    if form.validate_on_submit():
        patient = Patient(first_name=form.first_name.data, 
            second_name=form.second_name.data,
            phone_number=form.phone_number.data,
            patronymic=form.patronymic.data,
            medic=form.doctors.data,
            age=form.age.data,
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
@bp.route('/patient/<int:patient_id>/<int:funcc>', methods=['GET', 'POST'])
def view_patient(patient_id, funcc):
    # print(request.method)
    if request.method == "POST" and funcc==2:
        doc_id = request.form.get('doctor')
        print(doc_id)
        doctor = Doctor.query.filter_by(id=doc_id).first()
        if doctor:
            patient = Patient.query.filter_by(id=patient_id).first()
            print(patient)
            if patient.doctor_id == None:
                patient.doctor_id = doc_id
                db.session.add(patient)
                db.session.commit()
                flash('success')
                return redirect(url_for('patasys.view_patient',
                    patient_id=patient.id, funcc=1, 
                ))
            elif int(patient.doctor_id) != int(doc_id):
                patient.doctor_id = doc_id
                db.session.add(patient)
                db.session.commit()
                flash('success2')
                return redirect(url_for('patasys.view_patient',
                    patient_id=patient.id, funcc=1, 
                ))
            else:
                flash('У этого пациента уже назначен этот врач')
                return redirect(url_for('patasys.view_patient',
                    patient_id=patient.id, funcc=1, 
                ))
        else:
            flash('Такого врача нет')
            return redirect(url_for('patasys.index'))
    patient = Patient.query.filter_by(id=patient_id).first()
    doctor = Doctor.query.filter_by(id=patient.doctor_id).first()
    doctors = ''
    form = ''
    if (funcc == 2):
        doctors = Doctor.query.all()
    elif (funcc == 3):
        form = AddVisitForm()
        if form.validate_on_submit():
            tim = time.strptime(form.visit_time.data, "%Y-%m-%d %H:%M:%S")
            visit = Visit(
                visit_time = time.mktime(tim),
                patient_id = patient_id,
            )
            db.session.add(visit)
            db.session.commit()
            flash('Время успешно записано')
            return redirect(url_for('patasys.index'))
        
    
    context = {
        'patient': patient,
        'doctor': doctor,
        'doctors': doctors,
    }
    return render_template('patasys/view_patient.html', **context, form=form) 


@login_required
@bp.route('/add_service', methods=['GET', 'POST'])
def add_service():
    form = AddServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            cost=form.cost.data,
            code=form.code.data,
        )
        db.session.add(service)
        db.session.commit()
        flash('Услуга добавлена')
        return redirect(url_for('patasys.index'))
    return render_template('patasys/add_service.html', title='add service', form=form)
