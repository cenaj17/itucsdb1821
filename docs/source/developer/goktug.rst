Parts Implemented by Göktuğ Başaran
===================================

.. note:: All table creations exist in db_init.py file.

**************
Patients
**************

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS PATIENTS(
			ID SERIAL PRIMARY KEY,
			NAME VARCHAR(50) NOT NULL,
			AGE INTEGER,
			SEX BOOL DEFAULT FALSE, 
			TCKN VARCHAR NOT NULL,
			PHONE VARCHAR,
			CUR_COMPLAINT VARCHAR NOT NULL,
			INSURANCE INTEGER REFERENCES INSURANCE(INSURANCE_ID) 
				ON DELETE SET NULL 
				ON UPDATE CASCADE
		)
		
Insurance references Insurance table. If an insurance company is deleted
it is set to null, if an insurance company is updated, it is updated, as well.


2. Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

In order to read from patients table, we write a simple SELECT query with insurance table joined.

.. code-block:: python

    patients = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = "SELECT .NAME,AGE,SEX,TCKN,PHONE,CUR_COMPLAINT,INSURANCE.INSURANCE_NAME,.ID FROM ,INSURANCE WHERE .INSURANCE = INSURANCE.INSURANCE_ID ORDER BY .NAME ASC"
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        patients.append(row)
	cursor.close()

	
3. Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

In order to add a new patient, we write a simple INSERT query. We apply some validation in input boxes just in case.

.. code-block:: python

	if(name == "" or age == "" or tckn == "" or phone == "" or complaint == "" or insurance ==""):
		flash("Fill in the boxes")
		return redirect(url_for("patients_page"))
	else:
		insurance = "SELECT * FROM INSURANCE WHERE INSURANCE_NAME = \'{}\'".format(insurance)
		cursor.execute(insurance)
		connection.commit()
		result = cursor.fetchone()
		print(insurance)
		print(result)
		if not result == None and len(result) > 0:
			insurance_id = result[0]
			sex = True if sex == "Male" else False
			insert = "INSERT INTO (NAME,AGE,SEX,TCKN,PHONE,CUR_COMPLAINT,INSURANCE) VALUES(\'{}\',{},{},\'{}\',\'{}\',\'{}\',{});".format(
				name,age,sex,tckn,phone,complaint,insurance_id
				)
			cursor.execute(insert)
			connection.commit()
			return redirect(url_for("patients_page"))
		else:
			flash("Insurance company is unknown.",'warning')
			return redirect(url_for("patients_page"))

.. warning:: Insurance company must exist in order to insert a new patient.
			
4. Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

In order to update an existing patient, we need to find that patient first, if found, then it can be updated.
For this, 2 SQL queries are needed. One for finding, one for updating. This is not a must. It can be handled with only 1 query.
However, for a better user experience, for feedback, this structure is implemented.

.. code-block:: python
	
	#Selecting the patient.
	statement = "SELECT * FROM PATIENTS WHERE NAME = \'{}\'".format(name)
	cursor.execute(statement)
	connection.commit()
	result = cursor.fetchone()
	#Check if the result is empty.
	if not result == None and len(result) > 0:
		complaint = 'Flu'
		name = 'Foo'
		insert = "UPDATE PATIENTS SET CUR_COMPLAINT=\'{}\' WHERE name = \'{}\';".format(complaint,name)
			name,age,sex,tckn,phone,complaint,insurance_id
			)
		cursor.execute(insert)
		connection.commit()
		return redirect(url_for("patients_page"))
	else:
		flash("Insurance company is unknown.",'warning')
		return redirect(url_for("patients_page"))
		
.. warning:: Insurance company must exist in order to update a patient.
		
5. Deleting
~~~~~~~~~~~~~~~~~~~~~~~~

In order to delete a patient, we need to write a simple DELETE query.

.. code-block:: python

	name = 'Foo'
	statement = "DELETE FROM PATIENTS WHERE NAME=\'{}\'".format(name)
	cursor.execute(statement)
	connection.commit()
	cursor.close()
	
****************
Drug Companies
****************

1. Creation
~~~~~~~~~~~~~~~~~~~~

There are no foreign keys, this table is just an entity by itself.

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS DRUG_COMPANIES (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        FOUNDATION_YEAR INTEGER NOT NULL,
        FOUNDER VARCHAR NOT NULL,
        COUNTRY VARCHAR NOT NULL,
        WORKER_NUM INTEGER NOT NULL,
        FACTORY_NUM INTEGER NOT NULL
    )

2. Reading
~~~~~~~~~~~~~~~~~~~~

In order to read from drug companies table, we write a simple SELECT query.

.. code-block:: python

    companies = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT * FROM DRUG_COMPANIES"""""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        companies.append(row)
    cursor.close()
	
3. Adding
~~~~~~~~~~~~~~~~~~~~

In order to add a new company, we write a simple INSERT query. We apply some validation in input boxes just in case.

.. code-block:: python

	if(name=="" or year =="" or founder =="" or country == "" or factories ==""):
		flash("Please fill in all the boxes.",'warning')
		return redirect(url_for('drug_companies_page'))
	statement = "INSERT INTO PUBLIC.DRUG_COMPANIES(NAME,FOUNDATION_YEAR,FOUNDER,COUNTRY,WORKER_NUM,FACTORY_NUM) VALUES(\'{}\',{},\'{}\',\'{}\',{},{});".format(
		name,year,founder,country,workers,factories
	)
	print(statement)
	cursor.execute(statement)
	connection.commit()
	cursor.close()

4. Updating
~~~~~~~~~~~~~~~~~~~~

In order to update an existing company, we need to find that company first, if found, then it can be updated.
For this, 2 SQL queries are needed. One for finding, one for updating. This is not a must. It can be handled with only 1 query.
However, for a better user experience, for feedback, this structure is implemented.

.. code-block:: python

	statement = "SELECT * FROM DRUG_COMPANIES WHERE NAME = \'{}\'".format(name)
	cursor.execute(statement)
	connection.commit()
	result = cursor.fetchone()
	if not result == None and len(result)>0:
		comp_id = result[0]
		statement = "update public.drug_companies SET name=\'{}\',foundation_year={},FOUNDER=\'{}\',COUNTRY=\'{}\',WORKER_NUM={},FACTORY_NUM={} WHERE ID = {}".format(
		name,year,founder,country,workers,factories,comp_id
		)
		cursor.execute(statement)
		connection.commit()
		cursor.close()

5. Deleting
~~~~~~~~~~~~~~~~~~~~

In order to delete a company, we need to write a simple DELETE query.

.. code-block:: python

	name = 'Foo'
	statement = "DELETE FROM DRUG_COMPANIES WHERE NAME=\'{}\'".format(name)
	cursor.execute(statement)
	connection.commit()
	cursor.close()
	
****************
Drugs
****************

1. Creation
~~~~~~~~~~~~~~~~~~~~

In order to have drugs, we first need a helper table called Drug_Type. Drug type table is just 
an index table where every id corresponds to a drug type such as tablets, syrups etc.

.. code-block:: sql
	
    CREATE TABLE IF NOT EXISTS DRUGS(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR UNIQUE NOT NULL,
        COMPANY_ID INTEGER,
        SIZE INTEGER NOT NULL,
        SHELF_LIFE INTEGER NOT NULL,
        PRICE VARCHAR NOT NULL,
        TYPE INTEGER,
        CONSTRAINT c1 FOREIGN KEY (TYPE) REFERENCES DRUG_TYPE(ID) 
            ON DELETE SET NULL
            ON UPDATE CASCADE,
        CONSTRAINT c2 FOREIGN KEY (COMPANY_ID) REFERENCES DRUG_COMPANIES(ID)
            ON DELETE SET NULL
            ON UPDATE CASCADE
    );
	
	TYPE column references to DRUG_TYPE table. If a type is deleted, all the drugs that is that type have their types null,
	if a type is updated, all drugs that are that type are updated.
	
	COMPANY_ID column references to DRUG_COMPANIES table. The same stands for company_id column.

2. Reading
~~~~~~~~~~~~~~~~~~~~

In order to read from drug companies table, we write a simple SELECT query joined with drug_companies and drug_type.

.. code-block:: python

    drugs = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement= "SELECT DRUGS.name,DRUG_COMPANIES.name,size,shelf_life,price,DRUG_TYPE.name FROM DRUGS,DRUG_COMPANIES,DRUG_TYPE WHERE company_id=DRUG_COMPANIES.id AND type=DRUG_TYPE.id ORDER BY drugs.NAME ASC"
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        drugs.append(row)
    cursor.close()
	
3. Adding
~~~~~~~~~~~~~~~~~~~~

In order to add a new company, we write a simple INSERT query. We apply some validation in input boxes just in case.
We need to check if the drug company exists.

.. code-block:: python

	if(name=="" or company == "" or shelf =="" or size =="" or typ =="" or price == ""):
		flash("Please fill in all the boxes.",'warning')
		return redirect(url_for('drug_companies_page'))
	statement="SELECT * FROM DRUGS WHERE NAME= \'{}\'".format(name)
	print(statement)
	cursor.execute(statement)
	connection.commit()
	result = cursor.fetchone()
	if not result == None and len(result)>0:
		flash("The drug already exists, cannot insert.",'warning')
		cursor.close()
		return redirect(url_for("drugs_page"))
	else:
		statement = "SELECT * from drug_companies where NAME = \'{}\'".format(company)
		cursor.execute(statement)
		connection.commit()
		result = cursor.fetchone()
		if not result == None and len(result) > 0:
			company_id = result[0]
			statement = "SELECT * FROM DRUG_TYPE WHERE NAME = \'{}\'".format(typ)
			cursor.execute(statement)
			connection.commit()
			result = cursor.fetchone()
			if not result == None and len(result)>0:
				drug_type = result[0]
				statement = "INSERT INTO public.DRUGS(name,company_id,size,shelf_life,price,type) VALUES (\'{}\',{},{},{},\'{}\',{});".format(name,company_id,size,shelf,price,drug_type)
				print(statement)
				cursor.execute(statement)
				connection.commit()
				return redirect(url_for("drugs_page"))
			else:
				flash("Drug type is unknown. Please check again",'warning')
				return redirect(url_for("drugs_page"))
		else:
			flash("The Drug Company does not exists.",'warning')          
			return redirect(url_for("drugs_page"))

4. Updating
~~~~~~~~~~~~~~~~~~~~

In order to update an existing drug, we need to find that drug first, if found, then it can be updated if the drug company and tpe exist.
For this, 4 SQL queries are needed. One for finding the drug, one for finding the company, one for finding the type and one for updating. This is not a must. It can be handled with only 3 queries.
However, for a better user experience, for feedback, this structure is implemented.

.. code-block:: python

	name = 'Foo'
	statement="SELECT * FROM DRUGS WHERE NAME= \'{}\'".format(name)
	cursor.execute(statement)
	connection.commit()
	result = cursor.fetchone()
	if not result == None and len(result)==0:
		print("The drug does not exists, cannot update.")
		cursor.close()
		return redirect(url_for("drugs_page"))
	else:
		drug_id = result[0]
		statement = "SELECT * from drug_companies where NAME = \'{}\'".format(company)
		cursor.execute(statement)
		connection.commit()
		result = cursor.fetchone()
		if not result == None and len(result) > 0:
			company_id = result[0]
			statement = "SELECT * FROM DRUG_TYPE WHERE TYPE = \'{}\'".format(typ)
			cursor.execute(statement)
			connection.commit()
			result = cursor.fetchone()
			if not result == None and len(result)>0:
				drug_type = result[0]
				statement = "UPDATE public.drugs SET name=\'{}\',company_id={},size={},shelf_life={},price=\'{}\',type={} WHERE id = {};".format(name,company_id,size,shelf,price,typ,drug_id)
				cursor.execute(statement)
				connection.commit()
				return redirect(url_for("drugs_page"))
			else:
				flash("Drug type is unknown.",'warning')
				return redirect(url_for("drugs_page"))
		else:
			flash("The company does not exists.",'warning')

5. Deleting
~~~~~~~~~~~~~~~~~~~~

In order to delete a drug, we need to write a simple DELETE query.

.. code-block:: python
	name = 'Foo'
	statement = "DELETE FROM DRUGS WHERE NAME = \'{}\'".format(name)
	cursor.execute(statement)
	connection.commit()
	cursor.close()

********************
Extra Tables
********************

1. Drug Type
~~~~~~~~~~~~~~~~~~

Drug type table is just 
an index table where every id corresponds to a drug type such as tablets, syrups etc.

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS DRUG_TYPE(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL
    );
	
2. Allergies
~~~~~~~~~~~~~~~~~~

Allergies table is created to have a list of allergies.

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS ALLERGIES (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL
    );

3. Allergies Index
~~~~~~~~~~~~~~~~~~~~

Allergies index is the table where allergies are assigned to patients. This table is not visible anywhere on front-end, just yet.

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS ALLERGIE_INDEX (
        PATIENT_ID SERIAL PRIMARY KEY,
        ALLERGIES_ID INTEGER NOT NULL,
        CONSTRAINT c1 FOREIGN KEY (PATIENT_ID) REFERENCES PATIENTS(ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT c2 FOREIGN KEY (ALLERGIES_ID) REFERENCES ALLERGIES(ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )