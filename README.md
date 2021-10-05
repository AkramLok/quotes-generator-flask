#### Description:
Quoty is a web application that fetch, displays and even send quotes to others.
This project was completed in CS50 IDE where it was initially hosted and served.
New users start by registering a new account under "register" After filling in a unique email, first name, username, password, and confirming the password, then users are taken to the home. These values are immediately stored to the user table.

#### Video Demo:
https://youtu.be/9t9ybMygBmM

## Files
* 2 files written in python(application.py and helpers.py)
* 1 file in SQL(the database quotes.db)
* 1 file in CSS(styles.css)
* 1 file in JS(script.js)
* 12 files in HTML with some CSS and JS

## Database
The database has three principles tables(users, mails and quotes)

## APIs
i worked with 2 APIs:
* Type.fit that gives a list of quotes and their authors
* Lorem Picsum that generates images with your selected resolution

## Features
* register
* login
* logout
* homepage
* quote (login required)
* author (login required)
* mail (login required)
* mailbox (login required)
* change password (login required)

## Folders
- static: where is stored images and css file
- templates: where is stored all html files
- application.py: python file to help to run smoothy the program
- README.md: a markdown file introducing my web app
- requirements.txt: this file simply prescribes the packages on which this app will depend.

## Technologies
* python
* flask
* flask_session
* jinja
* sqlite
* sql
* CS50
* werkzeug
* time
* urllib
* requests
* html
* css
* javascript
* bootstrap
* flaticon

## Acknowledgements
* [codepen](https://codepen.io/trending)
* [Stack Overflow](https://stackoverflow.com)
* [geeksforgeeks](https://www.geeksforgeeks.org/)


## Setup
To run this project, use these commands:

```
$ cd [project folder]/
$ flask run
```
If you did it right, the web app should be online.

## Quitting the app
To stop the program, go to your terminal of choice. Hold the control key and press C. The program is now stopped, and if you refresh the web page, Chrome will give you an error.

## About cs50
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the computer science and the art of programming. This course teaches how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, security, and software engineering. Languages include C, Python, SQL, HTML, CSS, and JavaScript (for web development).
It helps you understand a lot of the core CS concepts, and then gives you the confidence to build cool projects. It is very difficult and fast-paced, but if you stick with it, I think it will pay off.
Thank you for all CS50 stuff.