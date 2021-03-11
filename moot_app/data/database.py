from os import environ
import psycopg2

def insert_booking(booking):
    sql = """INSERT INTO reg_earlybird_registrations(
        country_name,
        group_name,
        hoc_name,
        submitted_by_hoc,
        hoc_email,
        hoc_phone_number,
        hoc_address_line_1,
        hoc_address_line_2,
        number_of_earlybird_tickets) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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
            booking.country,                # country_name
            booking.org_name,               # group_name
            booking.contact_full_name,      # hoc_name
            booking.contact_position,       # submitted_by_hoc
            booking.contact_email,          # hoc_email
            booking.contact_phone,          # hoc_phone_number
            booking.org_address,            # hoc_address_line_1
            booking.org_address_postcode,   # hoc_address_line_2
            booking.participants))          # number_of_earlybird_tickets
        conn.commit()
        registration_number = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return registration_number
