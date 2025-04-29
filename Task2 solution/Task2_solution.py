
from flask import Flask, render_template, request, session 
import sqlite3

conn = sqlite3.connect("rolsa_technologies", check_same_thread=False) #used ai to remember how to connect the database to the solution and also how to stop a thread problem that was affecting some statements
cursor=conn.cursor()

app = Flask(__name__)
app.secret_key = "theywillneverknowthis"
@app.route('/')

#the variable logged_in will output to the page what they are logged in as
@app.route('/home',methods = ['POST','GET'])
def home():
    try:
        if session['email']:
            pass
    except:
        session['email'] = ""
    if request.method == 'POST': #the post method is used to handle inputs
        pass

    if request.method == 'GET': #the get method is used to load the page initially
        return render_template('/home.html',logged_in=logged_in()) #this line outputs to the website the page "home.html"


@app.route('/calculate_carbon_footprint',methods = ['POST','GET'])
def calculate_carbon_footprint():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        return render_template('/calculate_carbon_footprint.html',logged_in=logged_in())


@app.route('/installation_and_consultation_information',methods = ['POST','GET'])
def installation_and_consultation_information():
    if request.method == "POST":
        pass
    if request.method == 'GET':
        return render_template('/installation_and_consultation_information.html',logged_in=logged_in())


@app.route('/green_energy_products',methods = ['POST','GET'])
def green_energy_products():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        return render_template('/green_energy_products.html',logged_in=logged_in())


@app.route('/carbon_footprint_information',methods = ['POST','GET'])
def carbon_footprint_information():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        return render_template('/carbon_footprint_information.html',logged_in=logged_in())


@app.route('/sign_up',methods = ['POST','GET'])
def sign_up():
    if request.method == 'POST':
        pass_valid = False
        email_valid = False
        email = request.form.get('email') #gathering all information from the form on the page
        password = request.form.get('password')
        password2 = request.form.get('password_re-enter') #to check if the password is the same as the one entered before

        cursor.execute("SELECT * FROM tbl_users WHERE email = ?", (email,))
        check = cursor.fetchone()
        print("check")
        print(check)

        if email =="" or password =="": #checks for blank inputs
            error_message="must not leave inputs blank"
            return render_template('/sign_up.html',error_message=error_message,logged_in=logged_in())

        if len(password) < 8: #checks the length of the password
            error_message="password must have atleast 8 characters"

        s_character=False
        for i in range(len(password)):#checks that there is atleast 1 special character
            if password[i] in ["!","%","^","*","<",">","#","?"]:
                s_character = True
        if not s_character:
            error_message="password must have atleast 1 special character"
            return render_template('/sign_up.html',error_message=error_message,logged_in=logged_in())

        if check == None: #check is none when it returns nothing from the database, otherwise it will be the email in the database
            in_database = False
        else:
            in_database = True

        if password == password2: #checks if the passwords match
            pass_valid = True
        else:
            error_message = "Passwords must match eachother"
 
        if not in_database: #validates the request if it doesnt exist and returns the appropriate error message if it does
            email_valid = True
        else:
            error_message = "Account already exists"

        if email_valid and pass_valid: #final check to see if all checks were passed
            info = [email,password]
            print("Everything was VALID")
            #add to the database the new user
            cursor.execute("INSERT INTO tbl_users (email, password) VALUES (?, ?)", (email, password))
        else:
            return render_template('/sign_up.html',error_message=error_message,logged_in=logged_in())
        #print out table to check
        cursor.execute("SELECT * FROM tbl_users")
        conn.commit()
        table = cursor.fetchall()
        print(table)
        return render_template('/sign_in.html',logged_in=logged_in()) #sends user to the sign in page once they have signed up
    if request.method == 'GET':
        return render_template('/sign_up.html',logged_in=logged_in())


@app.route('/sign_in',methods = ['POST','GET'])
def sign_in(): #logs the user in when they get the email and password right
    if request.method == 'POST':
        email = request.form.get('email')#gets the email and password entered
        password = request.form.get('password')

        cursor.execute('SELECT * FROM tbl_users WHERE email=(?) AND password=(?)',(email,password)) #gets the data from the table that matches what the user put down
        print("IM IN IM IN IM IN IM IN")
        output = cursor.fetchall()
        print(output)
        if len(output) < 1:
            return render_template('/sign_in.html',error_message="Email or password is wrong try again",logged_in=logged_in())
        else:
            session['email'] = email
            print("session email is",session['email'])
            return render_template('/home.html',logged_in=logged_in())

    if request.method == 'GET':
        return render_template('/sign_in.html')


@app.route('/manage_bookings',methods = ['POST','GET'])
def manage_bookings():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        return render_template('/manage_bookings.html',logged_in=logged_in())

@app.route('/booking',methods = ['POST','GET'])
def booking():
    if request.method == 'POST':
        print(request.form.get('type'))
    if request.method == 'GET':
        return render_template('/booking.html',logged_in=logged_in())

def logged_in(): #function that outputs a message if logged in and outputs a blank string if not
    if session['email'] != "":
        message = f"logged in as {session['email']}"
        return(message)
    else:
        return("")

conn.execute("""
CREATE TABLE IF NOT EXISTS tbl_users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT,
payment_info TEXT
);
"""
    ) #creates the tables to store the data on if they dont already exist

conn.execute("""
CREATE TABLE IF NOT EXISTS tbl_bookings(
booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
type TEXT,
time DATE,
FOREIGN KEY (user_id) REFERENCES tbl_users (user_id)
);
"""
    )
app.debug = True
app.run()
session['email'] = "a"
logged_in = ""
