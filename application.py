import os
import random
import string
import time
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from helpers import apology, get_quotes, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///quotes.db")


@app.route("/pass", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":
        # return to apology when some condition is not respected
        password = request.form.get('password')
        if not password:
            return apology("set password")
        if len(password) < 8:
            return apology("Make sure your password is at least 8 letters")
        elif re.search('[0-9]', password) is None:
            return apology("Make sure your password has a number in it")
        elif re.search('[A-Z]', password) is None:
            return apology("Make sure your password has a capital letter in it")
        if not request.form.get('confirmation'):
            return apology("where confirmation password?", 400)
        if request.form['password'] != request.form['confirmation']:
            return apology("confirmation == password", 400)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(password), session["user_id"])
        return redirect("/")
    else:
        # get random password pf length 8 with letters, digits, and symbols
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(8))
        return render_template("passchange.html",password = password)


@app.route("/author", methods=["GET", "POST"])
def author():
    if request.method == "POST":
        # return to apology when some condition is not respected
        author = request.form.get("author")
        if not author:
            return apology("must write name", 400)
        quotes = get_quotes(author.lower())
        if not quotes:
            return apology("must provide valid author name", 400)
        auth = author.capitalize();
        return render_template("authored.html",quotes = quotes,auth=auth)
    else:
        return render_template("author.html")

@app.route("/search")
def search():
    quotes = db.execute("SELECT DISTINCT(author) AS author,COUNT(text) AS number FROM quotes WHERE author LIKE ? GROUP BY author;", "%" + request.args.get("q") + "%")
    return render_template("search.html", quotes=quotes)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user"] = rows[0]["username"];

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # accessing with post method
    if request.method == "POST":
        # return to apology when some condition is not respected
        username = request.form.get('username')
        check_username = db.execute("SELECT username FROM users WHERE username = ?", username)
        if not username:
            return apology("must provide username already existed?", 400)
        if check_username:
            return apology("username already taken", 400)
        password = request.form.get('password')
        if not password:
            return apology("set password")
        if len(password) < 8:
            return apology("Make sure your password is at least 8 letters")
        elif re.search('[0-9]', password) is None:
            return apology("Make sure your password has a number in it")
        elif re.search('[A-Z]', password) is None:
            return apology("Make sure your password has a capital letter in it")
        if not request.form.get('confirmation'):
            return apology("where confirmation password?", 400)
        if request.form['password'] != request.form['confirmation']:
            return apology("confirmation == password", 400)
        db.execute("INSERT INTO users (username,hash) VALUES(?, ?)", username, generate_password_hash(password))
        return redirect("/login")


@app.route("/inbox", methods=['GET', 'POST'])
@login_required
def inbox():
    if request.method == 'GET':
        emails = db.execute("SELECT * FROM mails WHERE recipient=:recipient ORDER BY datetime DESC;", recipient=session['user_id'])
        ls = []
        time_list = []
        for row in emails:
            sender = db.execute("SELECT username FROM users WHERE id=:id", id=row['sender'])
            username = sender[0]['username']
            subject = row['subject']
            date = str(row['datetime'])
            date_now = db.execute("SELECT datetime('now') AS now;")
            date_now = date_now[0]['now']
            message = row['message']
            mail_id = row['id']
            quote_id = row['quote_id']
            print(quote_id)
            read = row['read']
            time = (datetime.strptime(date_now,'%Y-%m-%d %H:%M:%S') - datetime.strptime(date,'%Y-%m-%d %H:%M:%S')).total_seconds()
            day = time // (24 * 3600)
            time = time % (24 * 3600)
            hour = time // 3600
            time %= 3600
            minutes = time // 60
            time_list = [int(day),int(hour),int(minutes)]
            if quote_id:
                text = db.execute("SELECT * FROM quotes WHERE id = ?;",quote_id)
                ls.append([username, subject, date, message, read, mail_id, text[0]["text"],text[0]["author"],time_list])
            else:
                ls.append([username, subject, date, message, read, mail_id,None,None,time_list])

        new_mail = False
        old_mail = False
        for row in ls:
            if row[4] == 0:
                new_mail = True
            if row[4] == 1:
                old_mail = True
        return render_template("inbox.html", mails=ls, new_mail=new_mail, old_mail=old_mail)
    else:
        delete = request.form.get('delete')
        read = request.form.get('read')
        if delete:
            # user wants to delete a mail
            db.execute("DELETE FROM mails WHERE id=:mail_id", mail_id=delete)
        elif read:
            s = db.execute("SELECT read FROM mails WHERE id=:id", id=read)
            state = s[0]['read']
            if state == 0:
                db.execute("UPDATE mails SET read=1 WHERE id=:id;", id=read)
            else:
                db.execute("UPDATE mails SET read=0 WHERE id=:id;", id=read)
        return redirect('/inbox')


@app.route("/send", methods=["GET", "POST"])
@login_required
def send():
    if request.method == "GET":
        return render_template("send.html")
    else:
        global state

        message = request.form.get("message")
        subject = request.form.get("subject")
        recipient = request.form.get("recipient")
        if request.form.get("quote"):
            quote_id = int(request.form.get("quote"))
        sender_id = session['user_id']

        # get the id from the recipient (if one exists)
        result = db.execute("SELECT id FROM users WHERE username=:name", name=recipient)
        if not result:
            state = 1 # user not found
            return redirect("/")

        recipient_id = result[0]['id']
        state = 2
        if request.form.get("quote"):
            db.execute("INSERT INTO [mails] ([message], [subject], [quote_id], [recipient], [sender], [datetime], [read]) VALUES (:message, :subject, :quote_id, :recipient, :sender, :datetime, 0);", message=message, subject=subject, quote_id=quote_id+1, recipient=recipient_id, sender=sender_id, datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            db.execute("INSERT INTO [mails] ([message], [subject], [recipient], [sender], [datetime], [read]) VALUES (:message, :subject, :recipient, :sender, :datetime, 0);", message=message, subject=subject, recipient=recipient_id, sender=sender_id, datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return redirect("/")


# state of the index page
state = 0 # 0 for nothing, 1 for recipient not found, 2 for message sent

@app.route("/")
@login_required
def index():
    global state
    s = state
    state = 0

    emails = db.execute("SELECT * FROM mails WHERE recipient=:recipient ORDER BY datetime DESC;", recipient=session['user_id'])
    ls = []
    for row in emails:
        sender = db.execute("SELECT username FROM users WHERE id=:id", id=row['sender'])
        username = sender[0]['username']
        subject = row['subject']
        date = str(row['datetime'])
        message = row['message']
        mail_id = row['id']
        quote_id = row['quote_id']
        read = row['read']
        ls.append([username, subject, date, message, read, mail_id,quote_id])

    new_mail = False
    for row in ls:
        if row[4] == 0:
            new_mail = True

    winning_number = random.randint (1, 1643)
    rand_quote = db.execute("SELECT * FROM quotes WHERE id = ?;",winning_number)
    return render_template("index.html", state=s, new_mail=new_mail,quote=rand_quote[0])

changed_name = False
delete_all = False
changed_pw = False

states = {
    'changed_name': False,
    'delete_all': False,
    'changed_pw': False,
    'wrong_pw': False
}


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)