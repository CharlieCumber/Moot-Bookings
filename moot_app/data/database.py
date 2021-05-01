from os import environ
from moot_app.data.booking import Booking
import psycopg2

def get_all_bookings():
    sql = """SELECT registration_number,
        country_name,
        group_name,
        hoc_name,
        submitted_by_role,
        hoc_email,
        hoc_phone_number,
        hoc_address_line_1,
        hoc_postcode,
        number_of_earlybird_tickets,
        number_of_participants,
        number_of_ist,
        number_of_cmt
        FROM reg_earlybird_registrations ORDER BY registration_id;"""

    conn = None
    bookings = []

    try:
        conn = psycopg2.connect(
            user = environ.get('DATABASE_USERNAME'),
            password = environ.get('DATABASE_PASSWORD'),
            host = environ.get('DATABASE_HOST'),
            port = environ.get('DATABASE_PORT'),
            database = environ.get('DATABASE_NAME'))
        cur = conn.cursor()
        cur.execute(sql)
        for booking in cur.fetchall():
            bookings.append(Booking.fromDatabase(booking))
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return bookings

def insert_booking(booking):
    sql = """INSERT INTO earlybird_staging_table(
        country_name,
        group_name,
        hoc_name,
        submitted_by_role,
        hoc_email,
        hoc_phone_number,
        hoc_address_line_1,
        hoc_postcode,
        number_of_earlybird_tickets,
        number_of_participants,
        number_of_ist,
        number_of_cmt) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING registration_number;"""
    
    conn = None
    registration_number = None

    try:
        conn = psycopg2.connect(
            user = environ.get('DATABASE_USERNAME'),
            password = environ.get('DATABASE_PASSWORD'),
            host = environ.get('DATABASE_HOST'),
            port = environ.get('DATABASE_PORT'),
            database = environ.get('DATABASE_NAME'))
        cur = conn.cursor()
        cur.execute(sql, (
            booking.country,                    # country_name
            booking.org_name,                   # group_name
            booking.contact_full_name,          # hoc_name
            booking.contact_position,           # submitted_by_role
            booking.contact_email,              # hoc_email
            booking.contact_phone,              # hoc_phone_number
            booking.org_address,                # hoc_address_line_1
            booking.org_address_postcode,       # hoc_postcode
            booking.participants,               # number_of_earlybird_tickets
            booking.standard_participants,      # number_of_participants
            booking.standard_IST,               # number_of_ist
            booking.standard_CMT))              # number_of_cmt
        conn.commit()
        registration_number = cur.fetchone()[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return registration_number