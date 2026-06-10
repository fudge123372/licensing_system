import psycopg2
from datetime import date,timedelta
conn=psycopg2.connect(host='127.0.0.1',port=5432,user='postgres',password='1234',dbname='licensing_system')
cur = conn.cursor()


#register a user
def create_user(details):
    sql="""INSERT INTO users(full_name,email,phone_number,password,role)VALUES(%s,%s,%s,%s,%s)"""

    cur.execute(sql,details)
    conn.commit()

#add business
def create_business(details):
    sql="""INSERT INTO businesses(user_id,business_name,business_type,location)VALUES(%s,%s,%s,%s)"""

    cur.execute(sql,details)
    conn.commit()

#create application
def create_application(details):
    sql = """INSERT INTO applications(business_id,application_type)VALUES(%s,%s)"""

    cur.execute(sql,details)
    conn.commit()

#view businesses
def get_businesses():
    cur.execute("SELECT * FROM businesses")
    businesses = cur.fetchall()
    return businesses

#view applications
def get_applications():
    cur.execute("""SELECT applications.application_id,businesses.business_name,applications.application_type,applications.status FROM applications JOIN businesses ON applications.business_id = businesses.business_id""")
    applications=cur.fetchall()
    return applications

# login user
def login_user(email, password):
    sql = """ SELECT * FROM users WHERE email=%s AND password=%s """
    cur.execute(sql, (email, password))
    return cur.fetchone()

def approve_application(application_id):
    sql = """UPDATE applications SET status='Approved'WHERE application_id=%s"""
    cur.execute(sql, (application_id,))
    conn.commit()

def reject_application(application_id):

    sql = """UPDATE applications SET status='Rejected'WHERE application_id=%s"""
    cur.execute(sql, (application_id,))
    conn.commit()


def get_my_businesses(user_id):
    sql = """SELECT * FROM businesses WHERE user_id=%s"""
    cur.execute(sql, (user_id,))
    return cur.fetchall()

def get_my_applications(user_id):

    sql = """SELECT applications.application_id,businesses.business_name,applications.application_type,applications.status FROM applications JOIN businesses ON applications.business_id = businesses.business_id WHERE businesses.user_id = %s"""
    cur.execute(sql, (user_id,))
    return cur.fetchall()

def create_license(application_id):
    issue_date = date.today()
    expiry_date = issue_date + timedelta(days=365)
    license_number = f"LIC-{application_id}"
    sql = """INSERT INTO licenses(application_id,license_number,expiry_date)VALUES (%s,%s,%s)"""
    cur.execute(sql,(application_id,license_number,expiry_date))
    conn.commit()

def get_licenses():
    cur.execute("""SELECT * FROM licenses""")
    return cur.fetchall()

# users
def total_users():
    cur.execute("SELECT COUNT(*) FROM users")
    return cur.fetchone()[0]

#  businesses
def total_businesses():
    cur.execute("SELECT COUNT(*) FROM businesses")
    return cur.fetchone()[0]

# Total applications
def total_applications():
    cur.execute("SELECT COUNT(*) FROM applications")
    return cur.fetchone()[0]

# Pending 
def pending_applications():
    cur.execute("SELECT COUNT(*) FROM applications WHERE status='Pending'")
    return cur.fetchone()[0]

# Approved 
def approved_applications():
    cur.execute("SELECT COUNT(*) FROM applications WHERE status='Approved'")
    return cur.fetchone()[0]

# Rejected 
def rejected_applications():
    cur.execute("SELECT COUNT(*) FROM applications WHERE status='Rejected'")
    return cur.fetchone()[0]
