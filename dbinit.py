import os
import sys

import psycopg2 as dbapi2



INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS USERS (
        ID VARCHAR UNIQUE PRIMARY KEY,
        PASSWORD VARCHAR NOT NULL,
        STATUS INTEGER NOT NULL
    )""",
    # unique kalkması lazım sanki - primary de patlar primary id ve password olmalı olcak
    #GOKTUG
    #False == Male
    """CREATE TABLE IF NOT EXISTS PATIENTS (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(50) NOT NULL,
        AGE INTEGER,
        SEX BOOL DEFAULT FALSE, 
        TCKN VARCHAR NOT NULL,
        PHONE VARCHAR,
        CUR_COMPLAINT VARCHAR NOT NULL,
        INSURANCE INTEGER
    )
    """,
    """CREATE TABLE IF NOT EXISTS ALLERGIES (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS ALLERGIE_INDEX (
        PATIENT_ID INTEGER NOT NULL,
        ALLERGIES_ID INTEGER NOT NULL,
        CONSTRAINT c1 FOREIGN KEY (PATIENT_ID) REFERENCES PATIENTS(ID),
        CONSTRAINT c2 FOREIGN KEY (ALLERGIES_ID) REFERENCES ALLERGIES(ID)
    )""",

     """CREATE TABLE IF NOT EXISTS DRUG_COMPANIES (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        FOUNDATION_YEAR INTEGER NOT NULL,
        FOUNDER VARCHAR NOT NULL,
        COUNTRY VARCHAR NOT NULL,
        WORKER_NUM INTEGER NOT NULL,
        FACTORY_NUM INTEGER NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS DRUG_TYPE(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS DRUGS(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR UNIQUE NOT NULL,
        COMPANY_ID INTEGER NOT NULL,
        SIZE INTEGER NOT NULL,
        SHELF_LIFE INTEGER NOT NULL,
        PRICE VARCHAR NOT NULL,
        TYPE INTEGER NOT NULL,
        CONSTRAINT c1 FOREIGN KEY (TYPE) REFERENCES DRUG_TYPE(ID),
        CONSTRAINT c2 FOREIGN KEY (COMPANY_ID) REFERENCES DRUG_COMPANIES(ID)
    )""",
    # /GOKTUG

    #Ecem

     """
    CREATE TABLE IF NOT EXISTS HOSPITAL(
        HOSPITAL_ID SERIAL PRIMARY KEY,
        HOSPITAL_NAME VARCHAR,
        IS_PUBLIC BOOL DEFAULT TRUE,
        LOCATION VARCHAR NOT NULL,
        ADMINISTRATOR VARCHAR,
        TELEPHONE_NUMBER NUMERIC(11),
        AMBULANCE_COUNT INTEGER
    )
    """,

        """CREATE TABLE IF NOT EXISTS HOSPITAL_PERSONNEL (
        PERSONNEL_ID SERIAL PRIMARY KEY,
        WORKER_NAME VARCHAR,
        JOB_TITLE VARCHAR NOT NULL,
        JOB_EXPERIENCE INTEGER,
        WORK_DAYS INTEGER,
        PHONE_NUM VARCHAR,
        WORKING_FIELD VARCHAR,
        HOSPITAL_WORKED INTEGER NOT NULL,
        TCKN VARCHAR,
        FOREIGN KEY (HOSPITAL_WORKED) REFERENCES HOSPITAL(HOSPITAL_ID) 
    )""",


        """CREATE TABLE IF NOT EXISTS DAY_TABLE (
        GENERATED_KEY SERIAL PRIMARY KEY,
        PERSONNEL_ID INTEGER,
        SHIFT_BEGIN_DATE DATE,
        SHIFT_REPEAT_INTERVAL INTERVAL,
        SHIFT_HOURS INTERVAL,
        DAYSHIFT BOOL,
        EMERGENCY_AREA_ASSIGNED VARCHAR, CHECK(EMERGENCY_AREA_ASSIGNED IN('Green','Yellow','Red')),
        FOREIGN KEY (PERSONNEL_ID) REFERENCES HOSPITAL_PERSONNEL
    )""",
        #emergency area assigned -> red yellow green


    """
    CREATE TABLE IF NOT EXISTS INSURANCE(
        INSURANCE_ID SERIAL PRIMARY KEY,
        INSURANCE_NAME VARCHAR,
        INSURANCE_TYPE VARCHAR
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS COVERANCE(
        INSURANCE INTEGER,
        HOSPITAL_COVERED INTEGER,
        SURGERY_COVERED BOOL,
        MAX_COST_DRUG INTEGER DEFAULT 0,
        FOREIGN KEY(HOSPITAL_COVERED) REFERENCES HOSPITAL,
        FOREIGN KEY(INSURANCE) REFERENCES INSURANCE(INSURANCE_ID)
    )
    """,

    #covered_hospitals -> all, public hospitals only, special privates included, none.

    # ATAKAN
    # job = 0 = pharmacist
    """
    CREATE TABLE IF NOT EXISTS pharmacy_personel (
        tckn INTEGER,
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        tel_num INTEGER,
        job BOOL NOT NULL,
        school VARCHAR,
        graduation_year INTEGER,
        years_worked INTEGER
    )
    """,
    """CREATE TABLE IF NOT EXISTS pharmacies (
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        location VARCHAR,
        pharmacist INTEGER,
        helper INTEGER,
        next_night_shift DATE,
        tel_num INTEGER,
        CONSTRAINT c1 FOREIGN KEY (helper) REFERENCES  pharmacy_personel(id),
        CONSTRAINT c2 FOREIGN KEY (pharmacist) REFERENCES  pharmacy_personel(id)
    )""",
    """
    CREATE TABLE IF NOT EXISTS pharmaceutical_warehouse (
        login_id INTEGER,
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        tel_num INTEGER,
        years_worked INTEGER,
        adress VARCHAR,
        region VARCHAR,
        carriers INTEGER
    )""",
    """
    CREATE TABLE IF NOT EXISTS pharmacy_inventory (
        drugs_id INTEGER REFERENCES DRUGS(ID),
        pharmacy_id INTEGER REFERENCES pharmacies(id),
        number INTEGER DEFAULT 0
    )""",
    """
    CREATE TABLE IF NOT EXISTS warehouse_inventory (
        drugs_id INTEGER REFERENCES DRUGS(ID),
        warehouse_id INTEGER REFERENCES pharmacies(id),
        number INTEGER DEFAULT 0
    )
    """,
    # $Ece Nur$

    """CREATE TABLE IF NOT EXISTS POLICLINICS (
        ID SERIAL PRIMARY KEY,
        HOSPITAL_ID INTEGER,
        RECEPTIONIST_ID INTEGER,
        NAME VARCHAR(50) NOT NULL,
        NUMBER_OF_EXAMINATION_ROOMS INTEGER DEFAULT 0,
        NUMBER_OF_OPERATION_ROOMS INTEGER DEFAULT 0,
        PRIVATE BOOL DEFAULT FALSE,
        IS_PEDIATRICS BOOL DEFAULT FALSE,
        FOREIGN KEY (HOSPITAL_ID) 
            REFERENCES HOSPITAL(HOSPITAL_ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (RECEPTIONIST_ID) 
            REFERENCES HOSPITAL_PERSONNEL(PERSONNEL_ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
    """,

    """CREATE TABLE IF NOT EXISTS DETAILED_POLICLINICS (
        ID  SERIAL PRIMARY KEY,
        HOSPITAL_ID INTEGER,
        POLICLINIC_ID INTEGER,
        DOCTOR_ID INTEGER,
        WORKING_HOURS VARCHAR(50),
        RESULT_HOURS VARCHAR(50),
        FOREIGN KEY (POLICLINIC_ID) 
            REFERENCES POLICLINICS(ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (DOCTOR_ID) 
            REFERENCES HOSPITAL_PERSONNEL(PERSONNEL_ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (HOSPITAL_ID) 
            REFERENCES HOSPITAL(HOSPITAL_ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
    """,

    """CREATE TABLE IF NOT EXISTS PRESCRIPTION (
        ID SERIAL PRIMARY KEY,
        HOSPITAL_ID INTEGER,
        DOCTOR_ID INTEGER,
        PATIENT_ID INTEGER,
        HOSPITAL_NAME VARCHAR,
        DOCTOR_NAME VARCHAR,
        PATIENT_NAME VARCHAR,
        PRESCRIPTION_DATE DATE NOT NULL,
        VALIDATION INTEGER DEFAULT 3,
        FOREIGN KEY (HOSPITAL_ID)  
            REFERENCES HOSPITAL(HOSPITAL_ID)
            ON DELETE SET NULL
            ON UPDATE SET NULL,
        FOREIGN KEY (DOCTOR_ID) 
            REFERENCES HOSPITAL_PERSONNEL(PERSONNEL_ID)
            ON DELETE SET NULL
            ON UPDATE SET NULL,
        FOREIGN KEY (PATIENT_ID) 
            REFERENCES PATIENTS(ID)
            ON DELETE CASCADE
            ON UPDATE SET NULL
    )
    """,

    """CREATE TABLE IF NOT EXISTS DETAILED_PRESCRIPTION(
        ID SERIAL PRIMARY KEY,
        PRESCRIPTION_ID INTEGER,
        DRUG_ID INTEGER,
        DRUG_NAME VARCHAR,
        DOSAGE_PER_TAKE INTEGER DEFAULT 1,
        TIMES_PER_DAY INTEGER DEFAULT 1, 
        DURATION INTEGER DEFAULT 3,
        REGULAR BOOL DEFAULT FALSE,
        FOREIGN KEY (PRESCRIPTION_ID) 
            REFERENCES PRESCRIPTION(ID)
            ON DELETE CASCADE
            ON UPDATE RESTRICT,
        FOREIGN KEY (DRUG_ID) 
            REFERENCES DRUGS(ID)
            ON DELETE SET NULL
            ON UPDATE SET NULL
    )
    """,

    """CREATE TABLE IF NOT EXISTS EXAMINATION(
        ID SERIAL PRIMARY KEY,
        PRESCRIPTION_ID INTEGER,
        TYPE VARCHAR(30) NOT NULL,
        DURATION INTEGER,
        PLACE VARCHAR(30),
        FOREIGN KEY (PRESCRIPTION_ID) 
            REFERENCES PRESCRIPTION(ID)
            ON DELETE CASCADE
            ON UPDATE RESTRICT
    )
    """
    # €Ece Nur€
]
def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)



def drop_table(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("DROP SCHEMA public CASCADE;CREATE SCHEMA public;")
        cursor.close()