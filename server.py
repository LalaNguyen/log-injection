"""""""""
IMPORT LIBRARY
"""""""""
from flask import Flask, render_template, redirect, url_for, request,flash
import datetime

"""""""""
FLASK CORE SETTINGS
"""""""""
app = Flask(__name__)
app.secret_key = 'some_secret'

"""""""""
FLASK ROUTINGS & FUNCTIONS
"""""""""
# use decorators to link the function to a url
@app.route('/home')
def home():
    """
        Render home page 
    """
    return "Congrats!"

@app.route('/')
def welcome():
    """
        Render '/' page 
    """
    return render_template('welcome.html')  # render a template

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
        Render Login page. Invoke banning scripts and check if user supplies 
        correct confidential.
    """
    errors_log = []
    if request.method == 'POST':
        host_addr, access_time = request.host.split(':'),datetime.datetime.now()
        status,duration = check_log(host_addr[0])
        # If user is not banned, proceed to normal login procedure
        if(status):
            # If user and password are incorrect, write down to log file.
            if request.form['username'] != 'admin' or request.form['password'] != 'admin':
                error = "[" + access_time.strftime('%m/%d/%Y %H:%M:%S') + "] Invalid Credentials. " + request.form['username'] + " failed to login with pass: " + request.form['password'] 
                write_log(reverse_autoescape(error))
            # Else redirect user to home page
            else:
                return redirect(url_for('home'))
        # If user is banned, raise back warning message.
        else:
            flash('Login failed. Your IP: '+ host_addr[0]+ ' is currently banned. Time-left estimation:'+str(30-duration.total_seconds()))
    # Render logs file back to user
    try:
        with open('user_log.txt','r') as infile:
            for line in infile.readlines():
                errors_log.append(line)
    except IOError as e:
        print e
    return render_template('login.html', errors=errors_log) 
    
def check_log(ip):
    """
        This function invokes user log files and check whether IP from the lastest line is matched.
        If IP is matched and status login is failed, ban that IP for 30 seconds.
    """
    last_line, err_code= "","failed"
    try:
        with open('user_log.txt','r') as infile:
            for line in infile.readlines():
                last_line = line
            # Check if last line has invalid attempt login
            if err_code in last_line:
                access,ctime = datetime.datetime.strptime(last_line[1:20], '%m/%d/%Y %H:%M:%S'),datetime.datetime.now()
                duration = ctime-access
                status = True if duration.total_seconds() > 30 else False
            # If error_code is not found, proceed on <-- this is the bug for log injections
            else:
                status,duration = True, 0
            return status, duration
    except IOError as e:
        print e    
        
def write_log(error):
    """ Receives a string and write it to log file. """
    try:
        with open('user_log.txt','ab') as outfile:
            outfile.write(error+'\n')
    except IOError as e:
        print e
           
def reverse_autoescape(s):
    """ Remove autoescape default from Flask for new line feed. """
    if "\\n" in s:
        return s.replace("\\n","\n")
    return s           
        
if __name__ == "__main__":
    app.run(debug=True)