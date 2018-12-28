Parts Implemented by Atakan Göl
================================

.. note:: All table creations exist in db_init.py file.

*****************
Pharmacy Personel
*****************

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

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

2. Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """ SELECT name,tel_num FROM pharmacy_personel WHERE (id ={} or id={})""".format(pharmacist_id,helper_id)
    cursor.execute(statement)
    connection.commit()
    employees = cursor.fetchall() 
    cursor.close()

Variables pharmacist_id and helper_id are already known.

3. Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    connection = db.connect(url)
	cursor = connection.cursor()
    statement = "UPDATE public.pharmacy_personel SET tel_num={}, years_worked={}	WHERE id = {};".format(tel,years,per_id)
    cursor.execute(statement)
    connection.commit()
    cursor.close()

In this example the personel which has it's id as pers_id, is eing updated. It's telephone number and years they worked at this pharmacy is changed.

*****************
Pharmacies
*****************

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS pharmacies (
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        location VARCHAR,
        pharmacist INTEGER REFERENCES  pharmacy_personel(id) ON DELETE SET NULL ON UPDATE CASCADE,
        helper INTEGER REFERENCES  pharmacy_personel(id) ON DELETE SET NULL ON UPDATE CASCADE,
        next_night_shift DATE,
        tel_num INTEGER
    )

helper and pharmacist references pharmacy_personel table. If an personel is deleted
they are set to null, if an personel is updated, they are updated, as well.

2. Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    date = str(datetime.datetime.now().date())
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT name,location,tel_num FROM pharmacies WHERE next_night_shift = '{}' """.format(date)
    cursor.execute(statement)
    connection.commit
    on_duty = cursor.fetchall()
    cursor.close()

In this example a list of all the pharmacies which's next night shift is today.

****************************
Pharmaceutical Warehouse
****************************

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS pharmaceutical_warehouse (
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        tel_num INTEGER,
        years_worked INTEGER,
        adress VARCHAR,
        region VARCHAR,
        carriers INTEGER
    )

2. Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT name,location,next_night_shift,tel_num,pharmacist,helper FROM pharmacies
                    WHERE id = '{}' """.format(pware_id) 
    cursor.execute(statement)
    connection.commit()
    phar_detail = cursor.fetchone()
    connection.close()

In this example we select the only pharmaceutical warehouse which has the same id as pware_id which was known.

**********************
Intermediate Tables - Inventory Tables
**********************

There are two tables used for the same purpose, Pharmacy Inventory and Pharmaceutical Warehouse Inventory tables.

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS pharmacy_inventory (
        drugs_id INTEGER REFERENCES DRUGS(ID) ON DELETE CASCADE ON UPDATE CASCADE,
        pharmacy_id INTEGER REFERENCES pharmacies(id) ON DELETE CASCADE ON UPDATE CASCADE,
        number INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS warehouse_inventory (
        drugs_id INTEGER REFERENCES DRUGS(ID) ON DELETE CASCADE ON UPDATE CASCADE,
        warehouse_id INTEGER REFERENCES pharmaceutical_warehouse(id) ON DELETE CASCADE ON UPDATE CASCADE,
        number INTEGER DEFAULT 0
    )

These tables refence both drugs table and pharmacies/pharmaceutical_warehouse tables.
They are deleted when either drugs or pharmacies/pharmaceutical_warehouse tables get deleted.
And updated if they are updated.


2. Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    connection = db.connect(url)
    cursor = connection.cursor()
    statement = "select NAME , number, drugs_id from DRUGS,pharmacy_inventory where pharmacy_inventory.pharmacy_id = {} and drugs_id = ID".format(id)
    cursor.execute(statement)
    connection.commit()
    inventory = cursor.fetchall()
    cursor.close()

This code returns all the inventory of the specified pharmacy.

3. Updating and Deleting
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    if new_value == 0:
        statement = "DELETE FROM public.pharmacy_inventory WHERE drugs_id={} and pharmacy_id = {};".format(inventory[k][2], id)
        del i[-1]
    else:
        statement = "UPDATE public.pharmacy_inventory SET number={} WHERE drugs_id={} and pharmacy_id = {};".format(new_value, inventory[k][2], id)

    cursor.execute(statement)
    connection.commit()
    cursor.close()

This code evaluates the new value of a specific drug of a specific pharmacy and either updates or deletes that entry.

