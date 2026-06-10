import psycopg2
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
    sql = """ SELECT * FROM users WHERE email=%s AND password=% """
    cur.execute(sql, (email, password))
    return cur.fetchone()