import sqlite3
from flask import Flask, render_template, request, g, session, redirect, url_for, escape

#DATA
DATABASE="./assignment3.db"

#Connects to the DATABASE file
def get_db():
    # if there is a database, use it
    db = getattr(g, '_database', None)
    if db is None:
        # otherwise, create a database to use
        db = g._database = sqlite3.connect(DATABASE)
    return db

# converts the tuples from get_db() into dictionaries
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# given a query, executes and returns the result
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#APP
app = Flask(__name__)
app.secret_key=b'secretkey'

# tears down the database connection when flask app closes.
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # close the database if we are connected to it
        db.close()

def cannot_view(): #error page, when you don't have permission to view.
    return '''
                <form action ="/">
                <p>You cannot view this page! 
                <p><input value ="Go back to Homepage!" type = "submit">
                </form>
                '''

@app.route('/')
def index():
    if 'student' in session: #will render template for students homepage view
        db = get_db()
        db.row_factory=make_dicts
        remark = query_db('SELECT * FROM Remarks where username==?', [session['student']], one=False)
        db.close()
        return render_template('student_index.html', student=session['student'], remark=remark)
    elif 'instructor' in session: #instructor  #will render instructor homepage view
        return render_template('instructor_index.html', instructor=session['instructor'])
    else: #not logged in
        return render_template('index.html') #homepage for guests viewing the site.

@app.route('/register', methods=['GET', 'POST'])
def register():
    #will not allow logged in users to see register page.
    if ('student' in session or 'instructor' in session):
        return cannot_view()

    if request.method=='POST':
        db = get_db()
        db.row_factory=make_dicts
        new_user = request.form
        if (new_user['username'] == "" or new_user['password'] == ""): #if inputed empty username/password
            return '''
                        <form action ="/register">
                        <p>This username/password cannot be empty! Try again!"
                        <p><input value ="Back to Register page" type = "submit">
                        </form>
                        ''' 
                        #asked to try again!
        sql = """ 
            SELECT *
            FROM Users
            """#selecting all users and checking if similar username in database.
        accs = query_db(sql, args=(), one=False)
        # What if input none for username and password ?need to add some cases here
        for acc in accs:
            if acc['username'] == new_user['username']:
                return '''
                        <form action ="/register">
                        <p>This username already exists! Try a new one!"
                        <p><input value ="Back to Register page" type = "submit">
                        </form>
                        '''
        num_accs = len(accs) + 1 
        cur = db.cursor()
        #inserting to user table
        cur.execute('INSERT INTO Users VALUES (?, ?, ?, ?)', [num_accs, new_user['username'], new_user['password'], new_user['type']])
        #if user is of type student
        if request.form['type'] == 'student':
            sql = """
                SELECT *
                FROM Students
                """
            num_students = len(query_db(sql, args=(), one=False)) + 1 #new student id
            #insert into students table
            cur.execute('INSERT INTO Students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [
                num_students, new_user['username'], new_user['fname'], new_user['lname'],
                0, 0, 0, 0, 0, 0, 0, 0
            ]) #inserting into students table of new user.
        #type instructor => add to instructor table
        else: #inserting into instructors table of new user info.
            sql = """
                SELECT *
                FROM Instructors
                """
            num_instrs = len(query_db(sql, args=(), one=False)) + 1 #new instructor id
            cur.execute('INSERT INTO Instructors VALUES (?, ?, ?, ?)', [
                num_instrs, new_user['username'], new_user['fname'], new_user['lname'],
            ]) #inserting into instructors table
        db.commit() #save changes
        cur.close()
        return '''
                <form action="/login">
                <p>Successfully registered!
                <p><input value ="Login Now!" type = "submit">
                </form>
                '''
    else:
        #register page
        return render_template("register.html")
    

@app.route('/login',methods=['GET','POST'])
def login():
    #already logged in
    if ('student' in session or 'instructor' in session):
        return cannot_view()

    #submitted
    if request.method=='POST': #button clicked to login.
        sql = """
			SELECT *
			FROM Users
			"""
        new_login = request.form
        results = query_db(sql, args=(), one=False)
        for result in results:
            if result[1]==new_login['username']: # authenticating user
                if result[2]==new_login['password']:
                    if result[3]=='student':
                        session['student'] = new_login['username']
                    else:
                        session['instructor'] = new_login['username']
                    return redirect(url_for('index'))
                else: #incorrect password
                    return '''
                            <form action="/login">
                            <p>Incorrect password! Try again
                            <p><input value ="Back to Login page" type = "submit">
                            </form>
                            '''
        #not found in database          
        return '''
                <form action ="/register">
                <p>Username does not exist.
                <p>New to here?
                <p><input value ="Register" type = "submit">
                </form>
               '''
    else:
        return render_template('login.html') #not logged in
        
@app.route('/logout')
def logout():
    if 'student' in session: #remove session of type student
	    session.pop('student', None)
    elif 'instructor' in session: #remove session of type instructor
        session.pop('instructor', None)
    else:
        #cannot logout when youre not even logged in..
        return '''
                <form action="/login">
                <p>"You are not logged in! You cannot log out!"
                <p><input value ="Back to Login page" type = "submit">
                </form>
                '''
    return redirect(url_for('index')) #redirect to homepage.

@app.route('/marks', methods=['GET', 'POST']) #post for remarks requests
def marks():
    if 'student' in session:
        db = get_db()
        db.row_factory=make_dicts
        if request.method=='POST': #remark request submitted from student
            remarks = query_db("SELECT * FROM Remarks", args=(), one=False)
            num_remarks = len(remarks) #gettting total remarks in remarks table to add new remark (unique id)
            num_remarks += 1
            cur = db.cursor()
            new_remark = request.form
            status = "ongoing"
            for rem in remarks:
                if rem['what']==new_remark['what'] and rem['username']==session['student']:
                    #already submitted request of this assignment (one per assessment, cannot request for another after)
                    return '''
                            <form action ="/marks">
                            <p>Already submitted a request of this assignment/quiz. Cannot resubmit!
                            <p><input value ="Go back to Marks page" type = "submit">
                            </form>
                            '''
            #adding new remark to table
            cur.execute('INSERT INTO Remarks VALUES (?, ?, ?, ?, ?)', [num_remarks, session['student'],
            new_remark['what'], new_remark['why'],status])
            db.commit()
            cur.close()
            db.close()
            return render_template('submit.html')
        else: #displaying marks for the specific student logged in
            student = query_db('SELECT * FROM Students where username==?', [session['student']], one=False)
            db.close()
            return render_template('marks.html', student=student)
    elif 'instructor' in session: #type instructor logged in, show class grades.
        db = get_db()
        db.row_factory=make_dicts
        student = query_db("SELECT * FROM Students", args=(), one=False)
        db.close()
        return render_template('allmark.html',student=student)
    else:
        return cannot_view()
             
@app.route('/viewrequests', methods=['GET', 'POST'])
def viewrequests(): #view remark requests from students to only instructors...
    if ('instructor' in session):
        db = get_db()
        db.row_factory=make_dicts
        remarks = query_db("SELECT * FROM Remarks", args=(), one=False)
        db.close()
        return render_template('viewrequests.html',remarks=remarks)
    else:
        return cannot_view()


@app.route('/remark', methods=['GET', 'POST'])
def remark():
    if not ('instructor' in session): #students cannot view remark page (for instructors only)
        return cannot_view()

    db = get_db()
    db.row_factory=make_dicts
    if request.method=='POST': #if button clicked for remark request
        cur = db.cursor()
        user = request.form
        if (user['newmark'] == ""):
            return "Marks field cannot be empty!"
        
        sql = ""
        #get info from database depending on the remark option selected from student
        if (user['which'] == "q1"):
            sql='UPDATE Students SET q1=? WHERE username==?'
        elif (user['which'] == "q2"):
            sql = 'UPDATE Students SET q2=? WHERE username==?'
        elif (user['which'] == "q3"):
            sql = 'UPDATE Students SET q3=? WHERE username==?'
        elif (user['which'] == "q4"):
            sql = 'UPDATE Students SET q4=? WHERE username==?'
        elif (user['which'] == "a1"):
            sql = 'UPDATE Students SET a1=? WHERE username==?'
        elif (user['which'] == "a2"):
            sql = 'UPDATE Students SET a2=? WHERE username==?'
        elif (user['which'] == "a3"):
            sql = 'UPDATE Students SET a3=? WHERE username==?'
        else:
            sql = 'UPDATE Students SET final=? WHERE username==?'
        cur.execute(sql,[user['newmark'],user['stud']]) #update student mark
        cur.execute('UPDATE Remarks SET status=? WHERE username==? and what==?',["closed",user['stud'],user['which']])
        #update remarks table (close request)
        db.commit() #save changes
        cur.close()
        db.close()
        return render_template('submit.html')
    else:
        student = query_db("SELECT * FROM Students", args=(), one=False)
        db.close()
        return render_template('remark.html',student=student)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'student' in session:
        db = get_db()
        db.row_factory=make_dicts
        if request.method=='POST': #submit pressed
            feedbacks = query_db("SELECT * FROM Feedback",  args=(), one=False)
            #find # of feedbacks in db
            num_feedbacks = len(feedbacks)
            num_feedbacks += 1
            cur = db.cursor()
            new_feedback = request.form
            cur.execute('INSERT INTO Feedback VALUES (?, ?, ?, ?, ?, ?)', [num_feedbacks,new_feedback['username'],
             new_feedback['q1'], new_feedback['q2'], new_feedback['q3'], new_feedback['q4']])
            db.commit()
            cur.close()
            db.close()
            return render_template('submit.html')
        else: #on page
            sql = """
                SELECT *
                FROM
                    ((SELECT username
                    FROM Users
                    WHERE type=="instructor")
                    NATURAL JOIN
                    Instructors)
                """
            instructors = query_db(sql, args=(), one=False)
            db.close()
            return render_template('feedback.html', instructors=instructors)
    elif 'instructor' in session:
        db = get_db()
        db.row_factory=make_dicts
        #getting feedbacks to instructor (specificly)
        feedbacks = query_db("SELECT * FROM Feedback where username==?", [session['instructor']], one=False)
        db.close()
        return render_template('viewfeedback.html',instructor=session['instructor'],feedbacks=feedbacks)
    else:
        return cannot_view() #error page

@app.route('/<file>')
#include only files that do not have their own functions that render their templates..
#render other templates where session type does not matter (for both student and instructors)
def render_templates(file):
    html_files = ['assignments', 'labs', 'lectures', 'links', 'news', 'office', 'team', 'tests']
    if file in html_files:
        return render_template(file + '.html')
    return '''
                <form action ="/">
                <p>This page does not exist!
                <p><input value ="Go back to Homepage!" type = "submit">
                </form>
                ''' #non existent route/page