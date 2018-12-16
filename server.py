from flask import Flask, render_template, redirect, url_for, flash, request, session,abort
from forms import FlaskForm, PatientSearchForm, LoginForm, G_PharmacySearchForm, HospitalSearchForm, HospitalAddForm
import datetime
import os
import psycopg2 as db
from dbinit import initialize, drop_table
from classes.hospital_personnel import *
app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW'

'''
connection = db.connect("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")
cursor = connection.cursor()
for statement in INIT_STATEMENTS:
	cursor.execute(statement)
connection.commit()
cursor.close()
'''

DEBUG = False

#DEBUG = True
# LIVE ICIN
if(DEBUG == False):
    url = os.getenv("DATABASE_URL")
else:
    # DENEME ICIN
    url = "dbname='postgres' user='postgres' host='localhost' password='hastayimpw'"
    initialize(url)
    # drop_table(url)


@app.route("/")
@app.route("/home")
def home_page():
    logged = True if session.get('logged_in') == True else False
    return render_template('home_page.html', logged=logged)


@app.route("/about")
def about_page():
    return render_template('about_page.html')


@app.route("/patients", methods=['GET', 'POST'])
def patients_page():
    patients = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = "SELECT PATIENTS.NAME,AGE,SEX,TCKN,PHONE,COMPLAINT,INSURANCE.INSURANCE_NAME FROM PATIENTS,INSURANCE_COMPANIES WHERE PATIENTS.INSURANCE = INSURANCE.INSURANCE_ID ORDER BY PATIENTS.NAME ASC"
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        patients.append(row)
    cursor.close()
    form = PatientSearchForm()
    if form.validate_on_submit():
        attr = form.select.data
        key = form.search.data
        result = []
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = "SELECT PATIENTS.NAME,AGE,SEX,TCKN,PHONE,COMPLAINT,INSURANCE.INSURANCE_NAME FROM PATIENTS,INSURANCE_COMPANIES WHERE PATIENTS.INSURANCE = INSURANCE.INSURANCE_ID AND CAST({} AS TEXT) ILIKE {} ORDER BY {} ASC".format(
            attr, "\'%" + key + "%\'", attr)
        #statement = """SELECT * FROM PATIENTS WHERE CAST({} AS TEXT) ILIKE {} ORDER BY {} ASC""".format(attr,"\'%" + key + "%\'", attr)
        cursor.execute(statement)
        connection.commit()
        for row in cursor:
            result.append(row)
        cursor.close()
        return render_template('patients_page.html', Patients=result, form=form)
    return render_template('patients_page.html', Patients=patients, form=form)


@app.route("/drugs")
def drugs_page():
    drugs = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = "SELECT DRUGS.name,DRUG_COMPANIES.name,size,shelf_life,price,DRUG_TYPE.name FROM DRUGS,DRUG_COMPANIES,DRUG_TYPE WHERE company_id=DRUG_COMPANIES.id AND type=DRUG_TYPE.id ORDER BY drugs.NAME ASC"
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        drugs.append(row)
    cursor.close()
    return render_template('drugs_page.html', Drugs=drugs)


@app.route("/drug_companies")
def drug_companies_page():
    companies = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT * FROM DRUG_COMPANIES"""""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        companies.append(row)
    cursor.close()
    return render_template('drug_companies_page.html', DrugCompanies=companies)


@app.route("/pharmacy", methods=['GET', 'POST'])
def pharmacy_page():
    date = str(datetime.datetime.now().date())
    print(date)
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT name,location,tel_num FROM pharmacies
						WHERE next_night_shift = '{}' """.format(date)
    cursor.execute(statement)
    connection.commit
    on_duty = cursor.fetchall()
    cursor.close()
    #id = session.get('id')
    #stat = session.get('status')
    # if (stat == 4):
    form1 = G_PharmacySearchForm()
    logged_in = session.get('logged_in')
    print(logged_in)
    if ((logged_in) and (session.get('status') == 4)):
        id = session.get('id')
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """SELECT id,name,tckn,school,graduation_year,years_worked,tel_num FROM pharmacy_personel
						WHERE tckn = '{}' """.format(id)
        cursor.execute(statement)
        connection.commit()
        phar_pers = cursor.fetchone()
        phar_id = phar_pers[0]

        statement = """SELECT name,location,next_night_shift,tel_num FROM pharmacies
						WHERE id = '{}' """.format(phar_id)
        cursor.execute(statement)
        connection.commit()
        phar_detail = cursor.fetchone()

        statement = """ SELECT pharmacy_personel.name,pharmacy_personel.tel_num FROM pharmacy_personel,pharmacies
						WHERE (pharmacies.id = {})""".format(phar_id)
        cursor.execute(statement)
        connection.commit()
        employees = cursor.fetchone()
        cursor.close()

        return render_template('pharmacy_page.html', on_duty=on_duty, id=phar_id, Personel=phar_pers, Pharma=phar_detail, Employees=employees, search_form=form1, logged_in=logged_in)
    else:
        if form1.validate_on_submit():
            attr = form1.select.data
            key = form1.search.data
            results = []
            connection = db.connect(url)
            cursor = connection.cursor()
            statement = """SELECT pharmacies.name,location,next_night_shift,pharmacies.tel_num,pharmacy_personel.name,pharmacies.id FROM pharmacies,pharmacy_personel WHERE """"" + \
                "CAST(pharmacies.{} AS TEXT) ILIKE  \'%{}%\' AND pharmacies.pharmacist = pharmacy_personel.id ORDER BY pharmacies.{} ASC".format(
                    attr, key, attr)
            # print(statement)
            cursor.execute(statement)
            connection.commit()
            for row in cursor:
                results.append(row)
            cursor.close()
            return render_template('pharmacy_page.html', on_duty=on_duty,   search_form=form1, logged_in=logged_in, results=results, searched=True)

        return render_template('pharmacy_page.html', on_duty=on_duty, search_form=form1, logged_in=logged_in, searched=False)
    return


@app.route("/inventory/<id>/<mode>")
def inventory_page(id, mode):
    #logged_in = session.get('logged_in')
    logged_in = True  # test

    connection = db.connect(url)
    cursor = connection.cursor()

    if (logged_in):  # pharma or pwarehouse
        if (mode == 'p'):
            statement = "select name from pharmacies where id={} ".format(id)
            cursor.execute(statement)
            connection.commit()
            name = cursor.fetchone()[0]

            #self = session.get('status')==4 and session.get['id']==id
            self = True
            if (self):
                statement = "select NAME , number from DRUGS,pharmacy_inventory where pharmacy_inventory.pharmacy_id = {} and drugs_id = ID".format(
                    id)
                cursor.execute(statement)
                connection.commit()
                inventory = cursor.fetchall()
                cursor.close()
                return render_template('inventory_page.html', self=True, name=name, results=inventory)
            else:
                statement = "select NAME from DRUGS,pharmacy_inventory where pharmacy_inventory.pharmacy_id = {} and drugs_id = ID".format(
                    id)
                cursor.execute(statement)
                connection.commit()
                inventory = cursor.fetchall()
                cursor.close()
                return render_template('inventory_page.html', self=False, name=name, results=inventory)

        elif (mode == 'w'):
            statement = "select name from pharmaceutical_warehouse where id={} ".format(
                id)
            cursor.execute(statement)
            connection.commit()
            name = cursor.fetchone()[0]
            statement = "select NAME , number from DRUGS,warehouse_inventory where warehouse_inventory.id = {} and drugs_id = ID".format(
                id)
            cursor.execute(statement)
            connection.commit()
            inventory = cursor.fetchall()
            cursor.close()
            return render_template('inventory_page.html', self=True, name=name, results=inventory)
        else:
            return redirect(url_for('home_page'))

    else:
        return redirect(url_for('home_page'))
    return


def hospital_page():
    hospitals = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """ SELECT * FROM HOSPITAL ORDER BY HOSPITAL_NAME"""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        hospitals.append(row)
    cursor.close()
    form=HospitalSearchForm()
    stat = session.get('status')
    if form.validate_on_submit():
        selection=form.selection.data
        data=form.search.data
        button=form.publicHos.data
        hospital_form=[]
        connection=db.connect(url)
        cursor =connection.cursor()
        if(button=='*'):
            statement="""SELECT * FROM HOSPITAL WHERE CAST({} AS TEXT) ILIKE  \'%{}%\' ORDER BY {} ASC """.format(selection, data , selection)
        else:
            statement="""SELECT * FROM HOSPITAL WHERE CAST({} AS TEXT) ILIKE  \'%{}%\' AND IS_PUBLIC={} ORDER BY {} ASC """.format(selection, data ,button, selection)
#        print(statement)
        cursor.execute(statement)
        connection.commit()
        for row in cursor:
            hospital_form.append(row)
        cursor.close()
        return render_template('hospital_page.html', hospital=hospital_form, form=form, stat=stat)
    return render_template('hospital_page.html', hospital=hospitals, form=form, stat=stat)
app.add_url_rule("/hospital", view_func=hospital_page, methods=['GET', 'POST'])

def add_hospital():
    status=session.get('status')
    status=7
    if status not in (1,7):
        return redirect(url_for('home_page'))
    hospitals=[]
    connection=db.connect(url)
    cursor=connection.cursor()
    statement = """ SELECT * FROM HOSPITAL ORDER BY HOSPITAL_NAME"""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        hospitals.append(row)
    cursor.close()
    hosAddForm=HospitalAddForm()
    if hosAddForm.validate_on_submit():
        hospital_name=hosAddForm.hospital_name.data
        is_public=hosAddForm.is_public.data
        location=hosAddForm.location.data
        administrator=hosAddForm.administrator.data
        telephone_number=hosAddForm.telephone_number.data
        ambulance_count=hosAddForm.ambulance_count.data
        connection = db.connect(url)
        cursor=connection.cursor()
        statement="""INSERT INTO HOSPITAL(HOSPITAL_NAME,IS_PUBLIC,LOCATION,ADMINISTRATOR,TELEPHONE_NUMBER, AMBULANCE_COUNT) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')""".format(hospital_name,is_public,location,administrator,telephone_number,ambulance_count)
        print(statement)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return redirect(url_for('hospital_page'))
    return render_template('hospital_add_page.html',hospital=hospitals,form=hosAddForm)
app.add_url_rule('/hospital/add_hospital',view_func=add_hospital, methods=['GET','POST'])

def single_personnel_page(personnel_id):
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM,HOSPITAL_WORKED,TCKN, WORKING_FIELD, HOSPITAL_NAME FROM HOSPITAL_PERSONNEL JOIN HOSPITAL ON HOSPITAL_WORKED=HOSPITAL_ID WHERE PERSONNEL_ID ='{}'""".format(
        personnel_id)
    cursor.execute(statement)
    connection.commit()
    db_person = cursor.fetchone()
    if db_person==None:
         abort(404)
    person = hospital_personnel(db_person[0], db_person[1], db_person[2], db_person[3],
                                db_person[4], db_person[5], db_person[6], db_person[7], db_person[8], db_person[9])
    cursor.close()
    return render_template('single_personnel_page.html', personnel=person, personnel_id=personnel_id)
app.add_url_rule("/emergency_shift/<int:personnel_id>",view_func=single_personnel_page,methods=['GET','POST'])



def hospital_personnel_sheet():
    workers = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM, WORKING_FIELD, HOSPITAL_NAME FROM HOSPITAL_PERSONNEL, HOSPITAL WHERE HOSPITAL_WORKED=HOSPITAL_ID GROUP BY PERSONNEL_ID, HOSPITAL_NAME"""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        workers.append(row)
    cursor.close()
    return render_template('hospital_personnel_page.html', hospital_personnel=workers)
app.add_url_rule("/hospital_personnel",
                 view_func=hospital_personnel_sheet, methods=['GET'])


def hospital_personnel_page(hospital_id):
    workers =[]
    connection = db.connect(url)
    cursor=connection.cursor()
    statement = statement = """SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE,
        JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM,WORKING_FIELD, HOSPITAL_WORKED, TCKN , HOSPITAL_NAME FROM HOSPITAL_PERSONNEL RIGHT JOIN HOSPITAL ON HOSPITAL_WORKED=HOSPITAL_ID WHERE HOSPITAL_WORKED =%s"""
    cursor.execute(statement,[hospital_id])
    connection.commit()
    for row in cursor:
        workers.append(row)
    cursor.close()
    return render_template('hospital_personnel_page.html',hospital_personnel=workers)
app.add_url_rule("/<int:hospital_id>/hospital_personnel",view_func=hospital_personnel_page,methods=["GET"])


def emergency_shift_page():
    data = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT HOSPITAL_PERSONNEL.PERSONNEL_ID, WORKER_NAME, SHIFT_BEGIN_DATE,SHIFT_REPEAT_INTERVAL,SHIFT_HOURS,DAYSHIFT ,EMERGENCY_AREA_ASSIGNED FROM DAY_TABLE LEFT JOIN HOSPITAL_PERSONNEL ON DAY_TABLE.PERSONNEL_ID=HOSPITAL_PERSONNEL.PERSONNEL_ID ORDER BY SHIFT_BEGIN_DATE"""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        data.append(row)
    cursor.close()
    return render_template('emergency_shift_page.html', data=data)


app.add_url_rule("/emergency_shift",
                 view_func=emergency_shift_page, methods=["GET"])


@app.route("/Prescription/<id>/", methods=['GET'])
def prescription_page(id):
    prescriptions = []
    date = datetime.datetime.now().date()
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT PRESCRIPTION.PRESCRIPTION_ID,HOSPITAL.HOSPITAL_NAME,HOSPITAL_PERSONNEL.WORKER_NAME,PRESCRIPTION.VALID_DATE FROM PRESCRIPTION,HOSPITAL_PERSONNEL,HOSPITAL 
		WHERE PATIENT_ID="""+"CAST("+id+"AS INTEGER)""" + """
		AND (HOSPITAL.HOSPITAL_ID = PRESCRIPTION.HOSPITAL_ID)
		AND (HOSPITAL_PERSONNEL.PERSONNEL_ID = PRESCRIPTION.DOCTOR_ID)
		ORDER BY PRESCRIPTION.VALID_DATE DESC
	"""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        prescriptions.append(row)
    cursor.close()
    return render_template('prescription.html', Prescriptions=prescriptions, id=id)


@app.route("/Prescription_Add/<id>/", methods=['GET', 'POST'])
def prescription_add_page(id):
    if(request.method == 'GET'):
        return render_template('prescription_add.html', id=id)
    else:
        drs_id = []
        hs_id =[]
        
        dr_id = int(request.form['dr_id'])
        h_name = request.form['hospital_name']
        valid = int(request.form['validity'])
    
        connection = db.connect(url)
        cursor = connection.cursor()
        hs_id = """SELECT HOSPITAL_ID FROM HOSPITAL
        WHERE HOSPITAL_NAME="""+"CAST("+ h_name+" AS VARCHAR)""" + """
        GROUP BY HOSPITAL_ID"""
        cursor.execute(hs_id)
        for row in cursor:
            hs_id = row
        h_id = hs_id[0]
        
        statement = """INSERT INTO PRESCRIPTION (HOSPITAL_ID,DOCTOR_ID,PATIENT_ID) VALUES (
            """ +"CAST("+str(h_id)+"AS INTEGER)""" + """,
            """ +"CAST("+str(dr_id)+"AS INTEGER)""" + """,
            """ +"CAST("+str(id)+"AS INTEGER)""" + """
        );
        """
        cursor.execute(statement)
        connection.commit()
        for row in cursor:
            print("my row:")
            print(row)
        cursor.close()
        print(dr_id)
        print(h_id)
        print(valid)
        return prescription_page(id)


@app.route("/Prescription/<id>/<pid>/", methods=['GET'])
def det_prescription_page(id, pid):
    drug = []
    examination = []
    date = datetime.datetime.now().date()
    connection = db.connect(url)
    cursor = connection.cursor()
    statement1 = """SELECT DETAILED_PRESCRIPTION.*,DRUGS.NAME FROM DETAILED_PRESCRIPTION,DRUGS,PRESCRIPTION
		WHERE PRESCRIPTION.PATIENT_ID="""+"CAST("+id+"AS INTEGER)""" + """
		AND PRESCRIPTION.PRESCRIPTION_ID =  PRESCRIPTION.PRESCRIPTION_ID
		
		AND DETAILED_PRESCRIPTION.PRESCRIPTION_ID ="""+"CAST("+pid+"AS INTEGER)""" + """
		AND (DRUGS.ID = DETAILED_PRESCRIPTION.DRUG_ID)
		GROUP BY DETAILED_PRESCRIPTION.ID,DRUGS.NAME
	"""
    cursor.execute(statement1)
    connection.commit()
    for row in cursor:
        drug.append(row)
    cursor.close()
    connection = db.connect(url)
    cursor = connection.cursor()
    statement2 = """SELECT EXAMINATION.* FROM EXAMINATION,PRESCRIPTION
		WHERE PRESCRIPTION.PATIENT_ID="""+"CAST("+id+"AS INTEGER)""" + """        
		AND EXAMINATION.PRESCRIPTION_ID ="""+"CAST("+pid+"AS INTEGER)""" + """
		GROUP BY EXAMINATION.ID
	"""
    cursor.execute(statement2)
    connection.commit()
    for row in cursor:
        examination.append(row)
    cursor.close()
    return render_template('detail_prescription.html', P_Drugs=drug, P_Examination=examination, id=id, pid=pid)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if session.get('logged_in'):
        return redirect(url_for('home_page'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            id = form.id.data
            pw = form.password.data
            try:
                connection = db.connect(url)
                cursor = connection.cursor()
                statement = """SELECT * FROM USERS WHERE ID = '%s'
						""" % id
                cursor.execute(statement)
                result = cursor.fetchone()
                if(result[1] == pw):
                    flash('You have been logged in!', 'success')
                    session['logged_in'] = True
                    session['id'] = id
                    session['status'] = result[2]
                    return redirect(url_for('home_page'))
                else:
                    flash(
                        'Login Unsuccessful. Please check username and password', 'danger')
            except db.DatabaseError:
                connection.rollback()
                flash('Login Unsuccessful. Please check username and password', 'danger')
            finally:
                connection.close()
        return render_template('login_page.html', title='Login', form=form)


@app.route("/logout")
def logout_page():
    session.pop('id', None)
    session['logged_in'] = False
    return redirect(url_for('home_page'))


if __name__ == "__main__":
    if(DEBUG):
        app.run(debug='True')
    else:
        app.run()
