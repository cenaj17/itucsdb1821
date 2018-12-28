Parts Implemented by Ayser Ecem Konu
====================================

.. note:: All table creations exist in db_init.py file.

**************
Hospitals
**************

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

        CREATE TABLE IF NOT EXISTS HOSPITAL(
        HOSPITAL_ID SERIAL PRIMARY KEY,
        HOSPITAL_NAME VARCHAR,
        IS_PUBLIC BOOL DEFAULT TRUE,
        LOCATION VARCHAR NOT NULL,
        ADMINISTRATOR VARCHAR,
        TELEPHONE_NUMBER NUMERIC(11),
        AMBULANCE_COUNT INTEGER
    )

This table has no foreign keys. Hospital id is incremented by database, user is not allowed
to enter hospital id for abstraction.

2. Reading
~~~~~~~~~~~~~~~~~~~~~~~~

Reading the table is done with no select in rendering page. If selection is done (form push method is used with search button)
another SELECT query will be executed.

.. code-block:: python

    hospitals = []
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """ SELECT * FROM HOSPITAL ORDER BY HOSPITAL_NAME"""
        cursor.execute(statement)
        connection.commit()
        rows=cursor.fetchall()
        for db_hosp in rows:
            hospitals.append(hospital(db_hosp[0],db_hosp[1],db_hosp[2],db_hosp[3],db_hosp[4],db_hosp[5],db_hosp[6]))
        cursor.close()
        form=HospitalSearchForm()
        status = session.get('status')
        #status=1
        delform=HospitalDeleteForm()
        if(request.method=='POST'):
            if form.validate_on_submit() and form.submit.data:
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
                rows=cursor.fetchall()
                for db_hosp in rows:
                    hospital_form.append(hospital(db_hosp[0],db_hosp[1],db_hosp[2],db_hosp[3],db_hosp[4],db_hosp[5],db_hosp[6]))
                cursor.close()
                return render_template('hospital_page.html', hospital=hospital_form, form=form,delform=delform, stat=status, len=len(hospital_form))

Entries of database is inserted into a class called Hospital inside classes folder.

.. code-block:: python

    class hospital:
        def __init__(self,hospital_id,hospital_name,is_public,location,administrator,telephone_number,ambulance_count):
            self.hospital_id=hospital_id
            self.hospital_name=hospital_name
            self.is_public=is_public
            self.location=location
            self.administrator=administrator
            self.telephone_number=telephone_number
            self.ambulance_count=ambulance_count


        def get_id(self):
            return self.hospital_id
        def get_name(self):
            return self.hospital_name
        def get_public(self):
            return self.is_public
        def get_location(self):
            return self.location
        def get_administrator(self):
            return self.administrator
        def get_telephone_number(self):
            return self.telephone_number
        def get_ambulance_count(self):
            return self.ambulance_count

Search validations are checked inside forms executable, by using form validators of wtforms

.. code-block:: python

    class HospitalSearchForm(FlaskForm):
        choices=[('HOSPITAL_NAME','Hospital Name'),
        ('LOCATION', 'Location'),
        ('ADMINISTRATOR','Administrator'),
        ('TELEPHONE_NUMBER','Phone Number')]
        selection=SelectField('Hospital Filter:',choices=choices)
        search=StringField('Keyword')
        publicHos=RadioField('Public Hospital? ',choices=[('True','Public'),('False','Private'),('*','Both')],validators=[DataRequired()])
        submit=SubmitField('Search')

3. Adding
~~~~~~~~~~~~~~~~~~~~~~~~

Adding a new hospital is maintained by the following Python function.INSERT query is done to add a new hospital.
.. code-block:: python
    def add_hospital():
        status=session.get('status')
        #status=1
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
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return redirect(url_for('hospital_page'))
        return render_template('hospital_add_page.html',hospital=hospitals,form=hosAddForm )
    app.add_url_rule('/hospital/add_hospital',view_func=add_hospital, methods=['GET','POST'])

Validating data is handled by form validators of wtforms, in forms executable.
.. code-block:: python
class HospitalAddForm(FlaskForm):
    hospital_name=StringField('Hospital Name',validators=[DataRequired()])
    is_public=RadioField('Public Hospital?',choices=[('True','Public'),('False','Private')],validators=[DataRequired()])
    location=StringField('Location')
    administrator=StringField('Administrator Name')
    telephone_number=StringField('Phone Number, 11 digit required')#,validators=[Length(min=11,max=11)])
    ambulance_count= StringField('Number of ambulances')
    submit=SubmitField('Insert')



4. Updating
~~~~~~~~~~~~~~~~~~~~~~~~

Editing an hospital is done by followed python function
.. code-block:: python
    def edit_hospital(hospital_id):
        status = session.get('status')
        #status=1
        if status not in (1,7):
            return redirect(url_for('home_page'))
        connection=db.connect(url)
        cursor=connection.cursor()
        statement = """ SELECT * FROM HOSPITAL WHERE HOSPITAL_ID={}""".format(hospital_id)
        cursor.execute(statement)
        connection.commit()
        db_hosp=cursor.fetchone()
        if db_hosp==None:
            abort(404)
        hospitalToedit=hospital(db_hosp[0],db_hosp[1],db_hosp[2],db_hosp[3],db_hosp[4],db_hosp[5],db_hosp[6])
        cursor.close()
        form=HospitalAddForm()
        if request.method=='POST':
            if form.validate_on_submit():
                hospital_name=form.hospital_name.data
                is_public=form.is_public.data
                location=form.location.data
                administrator=form.administrator.data
                telephone_number=form.telephone_number.data
                ambulance_count=form.ambulance_count.data
                connection = db.connect(url)
                cursor=connection.cursor()
                statement="""UPDATE HOSPITAL SET hospital_name='{}', is_public='{}', location='{}', administrator='{}', telephone_number='{}', ambulance_count='{}' WHERE HOSPITAL_ID={}""".format(hospital_name,is_public,location,administrator,telephone_number,ambulance_count, hospital_id)
                cursor.execute(statement)
                connection.commit()
                cursor.close()
                return redirect(url_for('hospital_page'))
        return render_template('hospital_edit_page.html',hospital=hospitalToedit,form=form)      
    app.add_url_rule('/<int:hospital_id>/edit_hospital',view_func=edit_hospital, methods=['GET','POST'])

Form update uses same form with hospital add, constrains are introduced with validators.

5. Deleting
~~~~~~~~~~~~~~~~~~~~~~~~

Delete query is written for hospital deletion.
Deleting will be done if push method is used by submitting delete button on hospital page.


.. code-block:: python
    delform=HospitalDeleteForm()
    if(request.method=='POST'):
        if delform.validate_on_submit() and delform.delete.data:
            del_list=request.form.getlist("del_hospitals")
            connection=db.connect(url)
            cursor=connection.cursor()
            if(len(del_list)>1):
                del_hospitals=tuple(del_list)
                statement="DELETE FROM hospital WHERE hospital_id IN {}".format(del_hospitals)
            else:
                del_hospitals=''.join(str(e) for e in del_list)
                statement="DELETE FROM hospital WHERE hospital_id = {}".format(del_hospitals)
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return redirect(url_for('hospital_page'))

Since multiple deletion was allowed with checkboxes, number of selected checkboxes will be considered.
If number of checkboxes are more than 1, multiple delete that iterates a tuple will be executed.

If one checkbox, or none was selected single deletion by transforming data into a string will be executed.

6. Showing All Workers of an Hospital
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All hospital personnel working in that hospital can be seen by clicking hospital name. This is done by getting hospital id by clicking
and after that, using the hospital id inside a search query. If session matches priveledged users, all functionality of hospital personnel will also
be available within that page.

.. code-block:: python
    def hospital_personnel_page(hospital_id):
        status=session.get('status')
        #status=1
        workers =[]
        connection = db.connect(url)
        cursor=connection.cursor()
        statement = statement = """SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE,
            JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM,WORKING_FIELD, HOSPITAL_WORKED, TCKN , HOSPITAL_NAME FROM HOSPITAL_PERSONNEL RIGHT JOIN HOSPITAL ON HOSPITAL_WORKED=HOSPITAL_ID WHERE HOSPITAL_WORKED =%s"""
        cursor.execute(statement,[hospital_id])
        connection.commit()
        data=cursor.fetchall()
        for db_hosp_personnel in data:
            workers.append(hospital_personnel(db_hosp_personnel[0],db_hosp_personnel[1],db_hosp_personnel[2],db_hosp_personnel[3],db_hosp_personnel[4],db_hosp_personnel[5],db_hosp_personnel[6],db_hosp_personnel[7],db_hosp_personnel[8],db_hosp_personnel[9]))
        cursor.close()
        searchForm=PersonnelSearchForm()
        delForm=PersonnelDeleteForm()
        if request.method=='POST':
            if searchForm.validate_on_submit():
                selection=searchForm.selection.data
                search=searchForm.search.data
                connection=db.connect(url)
                cursor =connection.cursor()
                personnel_form=[]
                statement="""SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM, WORKING_FIELD, HOSPITAL_WORKED,TCKN, HOSPITAL_NAME FROM HOSPITAL_PERSONNEL, HOSPITAL WHERE HOSPITAL_WORKED=HOSPITAL_ID AND CAST({} AS TEXT) ILIKE  \'%{}%\' ORDER BY {} ASC """.format(selection, search ,selection)
                cursor.execute(statement)
                connection.commit()
                rows=cursor.fetchall()
                for db_hosp_personnel in rows:
                    personnel_form.append(hospital_personnel(db_hosp_personnel[0],db_hosp_personnel[1],db_hosp_personnel[2],db_hosp_personnel[3],db_hosp_personnel[4],db_hosp_personnel[5],db_hosp_personnel[6],db_hosp_personnel[7],db_hosp_personnel[8],db_hosp_personnel[9]))
                cursor.close()
            if delForm.validate_on_submit() and delForm.delete.data:
                del_list=request.form.getlist("del_personnel")
                connection=db.connect(url)
                cursor=connection.cursor()
                if(len(del_list)>1):
                    del_personnel=tuple(del_list)
                    statement="""DELETE FROM HOSPITAL_PERSONNEL WHERE personnel_id IN {}""".format(del_personnel)
                else:
                    del_personnel=''.join(str(e) for e in del_list)
                    statement="""DELETE FROM HOSPITAL_PERSONNEL WHERE personnel_id = {}""".format(del_personnel)
                connection.commit()
                cursor.close()
                return redirect(url_for('hospital_personnel_sheet'))
            return render_template('hospital_personnel_page.html',hospital_personnel=personnel_form, searchForm=searchForm,delForm=delForm,stat=status)
        return render_template('hospital_personnel_page.html',hospital_personnel=workers, searchForm=searchForm, delForm=delForm, stat=status)
    app.add_url_rule("/<int:hospital_id>/hospital_personnel",view_func=hospital_personnel_page,methods=["GET","POST"])

status=1 was used as a debug statement in project development


*******************
Hospital Personnel
*******************

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS HOSPITAL_PERSONNEL (
            PERSONNEL_ID SERIAL PRIMARY KEY,
            WORKER_NAME VARCHAR,
            JOB_TITLE VARCHAR NOT NULL,
            JOB_EXPERIENCE INTEGER,
            WORK_DAYS INTEGER,
            PHONE_NUM VARCHAR,
            WORKING_FIELD VARCHAR,
            HOSPITAL_WORKED INTEGER NOT NULL,
            TCKN VARCHAR,
            FOREIGN KEY (HOSPITAL_WORKED) REFERENCES HOSPITAL(HOSPITAL_ID) ON DELETE CASCADE ON UPDATE CASCADE
        )

Foreign key referencing hospital table is introduced. If hospital id is deleted, personnel will also deleted, if its updated, personnel's hospital id
will be updated accordingly. Since personnel cannot work in an hospital that is no longer existing, personnel will also be deleted.

2. Reading
~~~~~~~~~~~~~~~~~~~~~~~~

Hospital personnel will have search form and search all function similar to hospitals.
SELECT query is used for reading entries.

.. code-block:: python
    status = session.get('status')
    #status=1
    workers = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM,WORKING_FIELD, HOSPITAL_WORKED, TCKN,  HOSPITAL_NAME FROM HOSPITAL_PERSONNEL, HOSPITAL WHERE HOSPITAL_WORKED=HOSPITAL_ID GROUP BY PERSONNEL_ID, HOSPITAL_NAME"""
    cursor.execute(statement)
    connection.commit()
    data=cursor.fetchall()
    for db_hosp_personnel in data:
        workers.append(hospital_personnel(db_hosp_personnel[0],db_hosp_personnel[1],db_hosp_personnel[2],db_hosp_personnel[3],db_hosp_personnel[4],db_hosp_personnel[5],db_hosp_personnel[6],db_hosp_personnel[7],db_hosp_personnel[8],db_hosp_personnel[9]))
    cursor.close()
    searchForm=PersonnelSearchForm()
    delForm=PersonnelDeleteForm()
    if request.method=='POST':
        if searchForm.validate_on_submit():
            selection=searchForm.selection.data
            search=searchForm.search.data
            connection=db.connect(url)
            cursor =connection.cursor()
            personnel_form=[]
            statement="""SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM, WORKING_FIELD, HOSPITAL_WORKED,TCKN, HOSPITAL_NAME FROM HOSPITAL_PERSONNEL, HOSPITAL WHERE HOSPITAL_WORKED=HOSPITAL_ID AND CAST({} AS TEXT) ILIKE  \'%{}%\' ORDER BY {} ASC """.format(selection, search ,selection)
            cursor.execute(statement)
            connection.commit()
            rows=cursor.fetchall()
            for db_hosp_personnel in rows:
                personnel_form.append(hospital_personnel(db_hosp_personnel[0],db_hosp_personnel[1],db_hosp_personnel[2],db_hosp_personnel[3],db_hosp_personnel[4],db_hosp_personnel[5],db_hosp_personnel[6],db_hosp_personnel[7],db_hosp_personnel[8],db_hosp_personnel[9]))
            cursor.close()
            return render_template('hospital_personnel_page.html',hospital_personnel=personnel_form, searchForm=searchForm,delForm=delForm,stat=status)

Entries of database is inserted into a class called hospital_personnel inside classes folder.

.. note:: Join methods are used to acquire hospital name for table reads.


.. code-block:: python

    class hospital_personnel:
    def __init__(self,personnel_id,worker_name,job_title,job_experience,work_days,phone_num,working_field,hospital_worked,tckn,hospital):
        self.personnel_id=personnel_id
        self.worker_name=worker_name
        self.job_title=job_title
        self.job_experience=job_experience
        self.work_days=work_days
        self.phone_num=phone_num
        self.working_field=working_field
        self.hospital_worked=hospital_worked
        self.tckn=tckn
        self.hospital =hospital

    def get_id(self):
        return self.personnel_id
    def get_name(self):
        return self.worker_name
    def get_title(self):
        return self.job_title
    def get_exp(self):
        return self.job_experience
    def get_days(self):
        return self.work_days
    def get_number(self):
        return self.phone_num
    def get_field(self):
        return self.working_field
    def get_hospital(self):
        return self.hospital_worked
    def get_tckn(self):
        return self.tckn
    def get_hospital_name(self):
        return self.hospital

Searchform is instantiated inside forms.py

.. code-block:: python

    class PersonnelSearchForm(FlaskForm):
        choices=[('WORKER_NAME','Personnel Name'),
        ('JOB_TITLE', 'Job Title'),
        ('JOB_EXPERIENCE','Job Experience'),
        ('WORK_DAYS','# of Days Worked'),
        ('PHONE_NUM','Contact Number'),
        ('WORK_DAYS','# of Days Worked'),
        ('WORKING_FIELD', 'Work Field')]
        selection=SelectField('Personnel Filter:', choices=choices)
        search=StringField('Keyword')
        submit=SubmitField('Search')

3. Adding
~~~~~~~~~~~~~~~~~~~~~~~~

Adding a new personnel is handled by another python function.

.. code-block:: python

    def add_personnel():
        status=session.get('status')
        #status=1
        if status not in (1,6,7):
            return redirect(url_for('home_page'))
        personnel=[]
        connection=db.connect(url)
        cursor=connection.cursor()
        statement = """SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM,WORKING_FIELD, HOSPITAL_WORKED, TCKN,  HOSPITAL_NAME FROM HOSPITAL_PERSONNEL, HOSPITAL WHERE HOSPITAL_WORKED=HOSPITAL_ID GROUP BY PERSONNEL_ID, HOSPITAL_NAME"""
        cursor.execute(statement)
        connection.commit()
        data=cursor.fetchall()
        for db_hosp_personnel in data:
            personnel.append(hospital_personnel(db_hosp_personnel[0],db_hosp_personnel[1],db_hosp_personnel[2],db_hosp_personnel[3],db_hosp_personnel[4],db_hosp_personnel[5],db_hosp_personnel[6],db_hosp_personnel[7],db_hosp_personnel[8],db_hosp_personnel[9]))
        cursor.close()
        addForm=PersonnelAddForm()
        if addForm.validate_on_submit():
            worker_name=addForm.worker_name.data
            job_title=addForm.job_title.data
            job_experience=addForm.job_experience.data
            work_days=addForm.work_days.data
            phone_num=addForm.phone_num.data
            working_field=addForm.working_field.data
            hospital_worked=addForm.hospital_worked.data
            tckn=addForm.tckn.data
            connection = db.connect(url)
            cursor=connection.cursor()
            statement="""INSERT INTO public.hospital_personnel(worker_name, job_title, job_experience, work_days, phone_num, working_field, hospital_worked, tckn)
        VALUES (\'{}\',\'{}\',\'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')""".format(worker_name,job_title,job_experience,work_days,phone_num,working_field,hospital_worked,tckn)
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return redirect(url_for('hospital_personnel_sheet'))
        return render_template('personnel_add_page.html',personnel=personnel,form=addForm, stat=status)
    app.add_url_rule('/hospital_personnel/add_personnel',view_func=add_personnel, methods=['GET','POST'])

Addform handles data validation using wtforms validators

.. code-block:: python

    class PersonnelAddForm(FlaskForm):
        worker_name=StringField('Personnel Name',validators=[DataRequired()])
        job_title=StringField('Job Title',validators=[DataRequired()])
        job_experience=StringField('Job Experience')
        work_days=StringField('Work Days')
        phone_num=StringField('Contact Number')
        working_field=StringField('Work Field')
        hospital_worked=StringField('Hospital Id')
        tckn=StringField('Tckn')
        submit=SubmitField('Insert')

4. Updating
~~~~~~~~~~~~~~~~~~~~~~~~

Updating can be done by clicking the personnel name on personnel page. This will
redirect user to single personnel page, where editing can also be done if session matches
specified sessions. If session does not match, only data will be shown.

addform is used for update aswell, due to the fact that validators and areas required match.

.. code-block:: python

    def single_personnel_page(personnel_id):
        status = session.get('status')
        #status=1
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM, WORKING_FIELD, HOSPITAL_WORKED, TCKN,  HOSPITAL_NAME FROM HOSPITAL_PERSONNEL JOIN HOSPITAL ON HOSPITAL_WORKED=HOSPITAL_ID WHERE PERSONNEL_ID ='{}'""".format(
            personnel_id)
        cursor.execute(statement)
        connection.commit()
        db_person = cursor.fetchone()
        if db_person==None:
            abort(404)
        person = hospital_personnel(db_person[0], db_person[1], db_person[2], db_person[3],
                                    db_person[4], db_person[5], db_person[6], db_person[7], db_person[8], db_person[9])
        cursor.close()
        form=PersonnelAddForm()
        if form.validate_on_submit():
            worker_name=form.worker_name.data
            job_title=form.job_title.data
            job_experience=form.job_experience.data
            work_days=form.work_days.data
            phone_num=form.phone_num.data
            working_field=form.working_field.data
            hospital_worked=form.hospital_worked.data
            tckn=form.tckn.data
            connection = db.connect(url)
            cursor=connection.cursor()
            statement="""UPDATE hospital_personnel SET worker_name='{}', job_title='{}', job_experience={}, work_days={}, phone_num='{}', working_field='{}', hospital_worked='{}', tckn='{}'
            WHERE personnel_id={}""".format(worker_name,job_title,job_experience,work_days,phone_num,working_field,hospital_worked,tckn,personnel_id)
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return redirect(url_for('hospital_personnel_sheet'))
        return render_template('single_personnel_page.html', personnel=person,form=form, stat=status,personnel_id=personnel_id)
    app.add_url_rule("/emergency_shift/<int:personnel_id>",view_func=single_personnel_page, methods=['GET','POST'])


5.Deleting
~~~~~~~~~~~~~~~~~~

Deleting will be done if push method is used by submitting delete button on personnel page.

.. code-block:: python
    if delForm.validate_on_submit() and delForm.delete.data:
        del_list=request.form.getlist("del_personnel")
        connection=db.connect(url)
        cursor=connection.cursor()
        if(len(del_list)>1):
            del_personnel=tuple(del_list)
            statement="""DELETE FROM HOSPITAL_PERSONNEL WHERE PERSONNEL_ID IN {}""".format(del_personnel)
        else:
            del_personnel=''.join(str(e) for e in del_list)
            statement="""DELETE FROM HOSPITAL_PERSONNEL WHERE PERSONNEL_ID = {}""".format(del_personnel)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return redirect(url_for('hospital_personnel_sheet'))

****************
Shift Table
****************

1. Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS DAY_TABLE (
            GENERATED_KEY SERIAL PRIMARY KEY,
            PERSONNEL_ID INTEGER,
            SHIFT_BEGIN_DATE DATE,
            SHIFT_REPEAT_INTERVAL INTERVAL,
            SHIFT_HOURS INTERVAL,
            DAYSHIFT BOOL,
            EMERGENCY_AREA_ASSIGNED VARCHAR, CHECK(EMERGENCY_AREA_ASSIGNED IN('Green','Yellow','Red')),
            FOREIGN KEY (PERSONNEL_ID) REFERENCES HOSPITAL_PERSONNEL ON DELETE CASCADE ON UPDATE CASCADE
        )
    
Day table has hospital personnel id as foreign key. If personnel id is deleted, shift will also deleted, if its updated, shift's personnel id
will be updated accordingly. Since there can not exist a shift for someone not working in there, deletion is a method to maintain conflicts on the database.

3 emergency areas exist in hospitals, emergency area is constricted by check statement, only Green, Yellow or Red can be assigned.

2. Reading
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def emergency_shift_page():
        data = []
        status = session.get('status')
        #status=1
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """SELECT GENERATED_KEY,HOSPITAL_PERSONNEL.PERSONNEL_ID, SHIFT_BEGIN_DATE,SHIFT_REPEAT_INTERVAL,SHIFT_HOURS,DAYSHIFT ,EMERGENCY_AREA_ASSIGNED, WORKER_NAME FROM DAY_TABLE LEFT JOIN HOSPITAL_PERSONNEL ON DAY_TABLE.PERSONNEL_ID=HOSPITAL_PERSONNEL.PERSONNEL_ID ORDER BY SHIFT_BEGIN_DATE"""
        cursor.execute(statement)
        connection.commit()
        fetcheddata=cursor.fetchall()
        for row in fetcheddata:
            data.append(shift_data(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
        cursor.close()

Left join is done to obtain names of personnel on duty from hospital personnel table.

Data read is inserted into class called shift_data inside classes folder.

.. code-block:: python

    class shift_data:
        def __init__(self,shift_id,personnel_id,shift_begin_date,shift_repeat_interval,shift_hours, dayshift,emergency_area_assigned, name):
            self.shift_id=shift_id
            self.personnel_id=personnel_id
            self.begin=shift_begin_date
            self.repeat=shift_repeat_interval
            self.hours=shift_hours
            self.dayshift=dayshift
            self.ea=emergency_area_assigned
            self.name=name
        def get_id(self):
            return self.shift_id
        def get_personnel_id(self):
            return self.personnel_id
        def get_begin(self):
            return self.begin
        def get_repeat(self):
            return self.repeat
        def get_hours(self):
            return self.hours
        def get_dayshift(self):
            return self.dayshift
        def get_ea(self):
            return self.ea
        def get_name(self):
            return self.name

3. Adding
~~~~~~~~~~~~~~~~~~~~

Adding is done using the form on shift sheet page.

.. code-block:: python

    class ShiftAddForm(FlaskForm):
        personnel_id=StringField('Personnel Id ',validators=[DataRequired()])
        shift_begin_date=StringField('Shift Begin Date YYYY-MM-DD')
        shift_repeat_interval=StringField('Shift Repeat Interval')
        shift_hours=StringField('Shift length -hours-')
        dayshift=RadioField('Shift in daytime?',choices=[('True','Daytime'),('False','Nighttime')],validators=[DataRequired()])
        emergency_area_assigned=StringField('Emergency area(Green, Yellow, Red)')
        submit=SubmitField('Insert')

Data validations from wtforms library are used for further checking of database. 
If checkbox is not specified, data will not be inserted into table.

.. code-block:: python

    form=ShiftAddForm()
    if form.validate_on_submit():
        personnel_id=form.personnel_id.data
        shift_begin_date=form.shift_begin_date.data
        shift_repeat_interval=form.shift_repeat_interval.data
        shift_hours=form.shift_hours.data
        dayshift=form.dayshift.data
        emergency_area_assigned=form.emergency_area_assigned.data
        connection =db.connect(url)
        cursor = connection.cursor()
        statement="""INSERT INTO day_table(
	personnel_id, shift_begin_date, shift_repeat_interval, shift_hours, dayshift, emergency_area_assigned)
	VALUES ( \'{}\',\'{}\',\'{}\', \'{}\', \'{}\', \'{}\')""".format(personnel_id,shift_begin_date,shift_repeat_interval,shift_hours,dayshift,emergency_area_assigned)
        print(statement)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return redirect(url_for('emergency_shift_page'))

Adding is done using insert query from data collected by push method into form.

4. Deleting
~~~~~~~~~~~~~~~~~~~~

Deleting is done similar to tables mentioned previously.

.. code-block:: python
    delform=HospitalDeleteForm()
    if delform.validate_on_submit():
            del_list=request.form.getlist("del_shift")
            connection=db.connect(url)
            cursor=connection.cursor()
            if(len(del_list)>1):
                del_intro=tuple(del_list)
                statement="""DELETE FROM DAY_TABLE WHERE GENERATED_KEY IN {}""".format(del_intro)
            else:
                del_intro=''.join(str(e) for e in del_list)
                statement="""DELETE FROM DAY_TABLE WHERE GENERATED_KEY ={}""".format(del_intro)
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return redirect(url_for('emergency_shift_page'))
    return render_template('emergency_shift_page.html',form=form,delform=delform, data=data,stat=status)


********************
Extra Tables
********************

1.Insurance
~~~~~~~~~~~~~~~~~~

.. code-block:: sql
    CREATE TABLE IF NOT EXISTS INSURANCE(
        INSURANCE_ID SERIAL PRIMARY KEY,
        INSURANCE_NAME VARCHAR,
        INSURANCE_TYPE VARCHAR
    )
    
Insurance is a table that is used for specifying insurance type that the patient has.

2. Coverance
~~~~~~~~~~~~~~~~~~

Coverence table is a table that connects insurances with hospitals.

.. code-block:: sql
    CREATE TABLE IF NOT EXISTS COVERANCE(
        INSURANCE INTEGER,
        HOSPITAL_COVERED INTEGER,
        SURGERY_COVERED BOOL,
        MAX_COST_DRUG INTEGER DEFAULT 0,
        FOREIGN KEY(HOSPITAL_COVERED) REFERENCES HOSPITAL ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY(INSURANCE) REFERENCES INSURANCE(INSURANCE_ID)  ON DELETE CASCADE ON UPDATE CASCADE
    )

Properties of insurances, such as covering surgeries and covering drugs are also included.

