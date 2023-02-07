import random
from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm


@app.route('/')
def index():

    return render_template('index.html', name='Terry')


@app.route('/equations')
def equations():

    def generate_equation():
        operators = ['+', '-', '*', '/']
        operator = random.choice(operators)
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        equation = str(num1) + operator + str(num2)
        correct_answer = eval(equation)
        wrong_answers = [correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10)]
        return equation, correct_answer, wrong_answers

    equation, correct_answer, wrong_answers = generate_equation()
    print("Equation:", equation)
    print("Correct Answer:", correct_answer)
    print("Wrong Answers:", wrong_answers)


    return render_template('equations.html', equation=equation, correct_answer=correct_answer, wrong_answers=wrong_answers, generate_equation=generate_equation(), score=0)



@app.route('/scores')
def posts():
    return 'These are your scores!'


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Submitted and Validated!')
        # Get data from the form
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
        # TODO: Check to see if there is a User with username and/or email
        if username == 'terryk':
            flash('That user already exists', 'danger')
            return redirect(url_for('signup'))
        # TODO: Create a new User with form data and add to database


        flash('Thank you for signing up!', 'success')
        
        # Redirect back to Home
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)
