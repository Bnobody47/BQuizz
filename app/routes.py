from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from app.models import User, QuizResult
from app.forms import LoginForm, RegistrationForm
from app.models import QuizQuestion
from flask import jsonify
from app.models import QuizQuestion


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
# Define sample quiz questions for Python, HTML, and CSS quizzes
python_questions = [
    {
        'question': 'What is the output of 2+2?',
        'options': ['4', '5', '6', 'None of the above'],
        'answer': '4'
    },
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'Rome', 'London', 'Berlin'],
        'answer': 'Paris'
    },
    {
        'question': 'What is the result of the expression 3*4?',
        'options': ['7', '12', '8', 'None of the above'],
        'answer': '12'
    },
    {
        'question': 'What is the output of the following code?\nprint("Hello, World!")',
        'options': ['Hello, World!', 'World', 'Hello', 'Error'],
        'answer': 'Hello, World!'
    },
    {
        'question': 'What is the largest integer in Python?',
        'options': ['int', 'long', 'float', 'bool'],
        'answer': 'int'
    },
    {
        'question': 'What is the result of the expression 5 * (3 + 2)?',
        'options': ['10', '15', '25', 'None of the above'],
        'answer': '25'
    },
    {
        'question': 'What is the output of the following code?\nprint(3 ** 2)',
        'options': ['6', '9', '5', 'None of the above'],
        'answer': '9'
    },
    {
        'question': 'Which keyword is used to define a function in Python?',
        'options': ['func', 'def', 'function', 'define'],
        'answer': 'def'
    },
    {
        'question': 'What is the correct way to write a comment in Python?',
        'options': ['# This is a comment', '// This is a comment', '// This is a comment //', '<!-- This is a comment -->'],
        'answer': '# This is a comment'
    },
    {
        'question': 'What is the output of the following code?\nprint("Hello" + " " + "World!")',
        'options': ['HelloWorld!', 'Hello World!', 'Hello + World!', 'Hello World'],
        'answer': 'Hello World!'
    },
    # Add more Python questions here
]

html_questions = [
    {
        'question': 'What does HTML stand for?',
        'options': ['Hyper Text Markup Language', 'Highly Text Markup Language', 'Hyperlinks and Text Markup Language', 'Home Tool Markup Language'],
        'answer': 'Hyper Text Markup Language'
    },
    {
        'question': 'Which HTML tag is used to define an unordered list?',
        'options': ['<ul>', '<ol>', '<li>', '<list>'],
        'answer': '<ul>'
    },
    {
        'question': 'Which HTML attribute specifies the URL of the page the link goes to?',
        'options': ['href', 'link', 'src', 'url'],
        'answer': 'href'
    },
    {
        'question': 'What does the HTML element <br> represent?',
        'options': ['Break line', 'Bold text', 'Paragraph', 'Image'],
        'answer': 'Break line'
    },
    {
        'question': 'Which HTML element is used to define important text?',
        'options': ['<important>', '<strong>', '<em>', '<i>'],
        'answer': '<strong>'
    },
    {
        'question': 'Which HTML element is used for creating a hyperlink?',
        'options': ['<a>', '<link>', '<href>', '<url>'],
        'answer': '<a>'
    },
    {
        'question': 'Which HTML tag is used to define a table?',
        'options': ['<table>', '<tb>', '<tr>', '<td>'],
        'answer': '<table>'
    },
    {
        'question': 'What does the HTML element <img> define?',
        'options': ['Image', 'Text', 'List', 'Table'],
        'answer': 'Image'
    },
    {
        'question': 'What does the HTML element <p> represent?',
        'options': ['Paragraph', 'Image', 'List', 'Table'],
        'answer': 'Paragraph'
    },
    {
        'question': 'Which HTML attribute specifies an alternative text for an image, if the image cannot be displayed?',
        'options': ['alt', 'title', 'src', 'href'],
        'answer': 'alt'
    },
    # Add more HTML questions here
]

css_questions = [
    {
        'question': 'What does CSS stand for?',
        'options': ['Creative Style Sheets', 'Cascading Style Sheets', 'Computer Style Sheets', 'Colorful Style Sheets'],
        'answer': 'Cascading Style Sheets'
    },
    {
        'question': 'Which CSS property is used to change the text color of an element?',
        'options': ['color', 'text-color', 'font-color', 'background-color'],
        'answer': 'color'
    },
    {
        'question': 'Which CSS property is used to control the spacing between elements?',
        'options': ['margin', 'padding', 'border', 'spacing'],
        'answer': 'margin'
    },
    {
        'question': 'What does the CSS property "display: none;" do?',
        'options': ['Hides the element', 'Makes the element visible', 'Adds a border to the element', 'Changes the font of the element'],
        'answer': 'Hides the element'
    },
    {
        'question': 'Which CSS property is used to set the background color of an element?',
        'options': ['background-color', 'color', 'bgcolor', 'background'],
        'answer': 'background-color'
    },
    {
        'question': 'Which CSS property is used to change the font size of an element?',
        'options': ['font-size', 'text-size', 'size', 'font-style'],
        'answer': 'font-size'
    },
    {
        'question': 'Which CSS property is used to change the font weight of an element?',
        'options': ['font-weight', 'text-weight', 'weight', 'font-style'],
        'answer': 'font-weight'
    },
    {
        'question': 'Which CSS property is used to change the background image of an element?',
        'options': ['background-image', 'image', 'background', 'bg-image'],
        'answer': 'background-image'
    },
    {
        'question': 'Which CSS property is used to set the width of an element?',
        'options': ['width', 'size', 'height', 'set-width'],
        'answer': 'width'
    },
    {
        'question': 'Which CSS property is used to make text bold?',
        'options': ['font-weight: bold', 'text-weight: bold', 'bold', 'font-style: bold'],
        'answer': 'font-weight: bold'
    },
    # Add more CSS questions here
]
@app.route('/quiz')
@login_required
def quiz():
    questions = QuizQuestion.query.all()
    return render_template('quiz.html', questions=questions)

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    score = 0
    total_questions = 0
    for question in request.form:
        total_questions += 1
        if request.form[question] == QuizQuestion.query.filter_by(id=question).first().correct_answer:
            score += 1
    user_result = QuizResult(user_id=current_user.id, score=score)
    db.session.add(user_result)
    db.session.commit()
    return redirect(url_for('quiz_results'))
@app.route('/api/quiz_questions')
def get_quiz_questions():
    questions = QuizQuestion.query.all()
    return jsonify({'questions': [question.serialize() for question in questions]})
