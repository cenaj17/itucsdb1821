import psycopg2 as dbapi2
import sys
import json
import os

path_url  = "dbname='db' user='postgres' host='localhost' password='1234'"

#function that takes the values passed (email, name, password and university major of a student)
#and inserts it as a row in Student table
def student_signup(email, password):
    tmp=False
    id=0
    connection = dbapi2.connect(path_url)
    cursor = connection.cursor()
    query = """INSERT INTO public."STUDENT"("EMAIL", "PASSWORD")
	VALUES ('{}', '{}') RETURNING "ID";""".format(email, password)
    try:
        cursor.execute(query)
        id = cursor.fetchone()
        connection.commit()
        id = int(id[0])
        tmp=True
    except Exception as err:
        if (err.pgcode == "23505"):
            print("E-mail is already being in use.")
            id=-1
            tmp=False
    finally:
        cursor.close()
        connection.close()

    return (tmp,id)


#function logging in to the student account
#taking email and password as values
def student_login(email, password):

    connection = dbapi2.connect(path_url)
    cursor = connection.cursor()
    query = """SELECT "ID" FROM public."STUDENT" where "EMAIL" = '{}' and "PASSWORD"='{}';""".format(email, password)
    cursor.execute(query)
    res = cursor.fetchone()
    if res:
        return (True, int(res[0]))
    
    query = """SELECT "ID" FROM public."STUDENT" where "EMAIL" = '{}' ;""".format(email)
    if res:
        print('Password entered is wrong.')
        return (False, int(res[0]))

    print("Create a new account.")

    return(False, -1)

#function which shows the student details 
#when the student id is provided
def student_profile(student_id):

    connection = dbapi2.connect(path_url)
    cursor = connection.cursor()    
    query ="""SELECT 
    S."ID" as id,
    S."NAME" as name,
    S."UNIVERSITY" as university,
	ARRAY_AGG( concat(SK."NAME", ':' ,SK."DESCRIPTION")) as skill_list
    from "STUDENT" S 
    left join "STUDENT_SKILL" SS on S."ID" = SS."STUDENT_ID" 
    left join "SKILL" SK on SS."SKILL_ID" = SK."ID"
	where S."ID" = {}
    GROUP BY S."ID",S."NAME",S."UNIVERSITY"
    """.format(student_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return(result)


def student_skill(student_id,skill_id):
    connection = db.connect(path_url)
    cursor = connection.cursor()
    statement = """INSERT INTO public."STUDENT_SKILL"(
	"STUDENT ID", "SKILL ID")
	VALUES ({}, {}) RETURNING "ID";""".format(student_id,skill_id)
    try:
        cursor.execute(statement)
        res = cursor.fetchall()
        connection.commit()
        flag = True
        try:

            id = res[0][0]
        except:
            print("no student with this id" )
            id=student_id
            flag=False

    except Exception as err:
        
        if (err.pgcode == "23503"):
            print("this skill or student doesnt exist")
            id=-1
            flag=False
        if (err.pgcode == "23505"):
            print("this student already has this skill")
            id=-1
            flag=False
        id=-1
        flag=False

    finally:
        cursor.close()
        connection.close()
        
    return (flag,id)

def student_university(student_id,department_id):
    connection = db.connect(path_url)
    cursor = connection.cursor()
    statement = """UPDATE public."STUDENT"
	SET "UNIVERSITY MAJOR"={}
	WHERE "ID"={} returning "ID";""".format(department_id,student_id)

    try:
        cursor.execute(statement)
        res = cursor.fetchall()
        #print(len(res))
        connection.commit()
        flag = True
        try:

            id = res[0][0]
        except:
            "no student with this id" 
            id=student_id
            flag=False
    except Exception as err:
        print_psycopg2_exception(err)
        if (err.pgcode == "23503"):
            print("no department with this id found")
            id=-1
            flag=False
    finally:
        cursor.close()
        connection.close()
        
    return (flag,id)

#employer signup function taking as values
#the company name, email and password
def signup_employer(email, password): 
    connection = db.connect(path_url)
    cursor = connection.cursor()
    query = """INSERT INTO public."EMPLOYER"(
	"EMAIL", "PASSWORD")
	VALUES ('{}', '{}') RETURNING "ID" ;""".format(email, password)
    try:
        cursor.execute(query)
        id = cursor.fetchone()
        connection.commit()
        id = int(id[0])
        tmp=True
    except Exception as err:
        if (err.pgcode == "23505"):
            print("E-mail is already being used.")
            id=-1
            tmp=False
    finally:
        cursor.close()
        connection.close()
    return (tmp, id)

#function that takes email and password
#as attributes in order to login
def login_employer(email, password):
    tmp=False
    connection = db.connect(path_url)
    cursor = connection.cursor()
    query = """SELECT "ID" FROM public."EMPLOYER" where "EMAIL" = '{}' and "PASSWORD"='{}';""".format(email, password)
    cursor.execute(query)
    tmp = cursor.fetchone()
    if tmp:
        return (True, int(tmp[0]))
    query = """SELECT "ID" FROM public."EMPLOYER" where "EMAIL" = '{}' ;""".format(email)
    if tmp:
        print('The entered password is wrong.')
        return (False, int(tmp[0]))
    print("Create a new account.")
    return(False,-1)  
