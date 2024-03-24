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
