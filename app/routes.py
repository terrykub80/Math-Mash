import random
import time
from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.forms import SignUpForm, LoginForm, ProblemForm, EditUserForm
from app.models import User, Score


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/myinfo')
def my_info():
    user = User.query.all()
    if not user:
        flash(f"A user with id {user.id} does not exist", "danger")
        return redirect(url_for('index'))
    return render_template('myinfo.html', user=user)



@app.route('/myinfo/<user_id>/edituser', methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    form = EditUserForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        User.update(user, email=email, username=username)
        return redirect(url_for('my_info', user_id=user_id))

    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    
    return render_template('edituser.html', user=user, form=form)


@app.route('/myinfo/<user_id>/deleteuser')
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    user.delete()
    flash(f"{user.username} has been deleted", "success-subtle")
    return redirect(url_for('index'))


@app.route('/equations')
def equations():

    return render_template('equations.html')



@app.route('/equations/random', methods=['GET', 'POST'])
def equations_random():
    form = ProblemForm()

    # def countdown(t):
    #     while t:
    #         mins, secs = divmod(t, 60)
    #         timer = '{:02d}:{:02d}'.format(mins, secs)
    #         print(timer, end="\r")
    #         time.sleep(1)
    #         t -= 1
            

    def generate_equation():
        operators = ['+', '-', '*', '/']
        operator = random.choice(operators)
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        equation = str(num1) + ' ' + operator + ' ' + str(num2)
        correct_answer = eval(equation)
        wrong_answers = [correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10)]
        return equation, correct_answer, wrong_answers
 
    equation, correct_answer, wrong_answers = generate_equation()


    def handle_answers():
        if form.answer == correct_answer:
            form.score += 1
            print(correct_answer)
        else:
            print(correct_answer)
        generate_equation()
        # return form.score


    if form.validate_on_submit:
        handle_answers()

    return render_template('random.html', equation=equation, correct_answer=correct_answer, generate_equation=generate_equation(), handle_answers=handle_answers(), form=form)


@app.route('/equations/addition')
def equations_addition():

    def generate_addition():
        operator = '+'
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        equation = str(num1) + ' ' + operator + ' ' + str(num2)
        correct_answer = eval(equation)
        wrong_answers = [correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10)]
        return equation, correct_answer, wrong_answers

    equation, correct_answer, wrong_answers = generate_addition()
    print("Equation:", equation)
    print("Correct Answer:", correct_answer)
    print("Wrong Answers:", wrong_answers)


    return render_template('addition.html', equation=equation, correct_answer=correct_answer, wrong_answers=wrong_answers, generate_addition=generate_addition(), score=0)


@app.route('/equations/subtraction')
def equations_subtraction():

    def generate_subtraction():
        operator = '-'
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        equation = str(num1) + operator + str(num2)
        correct_answer = eval(equation)
        wrong_answers = [correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10)]
        return equation, correct_answer, wrong_answers

    equation, correct_answer, wrong_answers = generate_subtraction()
    print("Equation:", equation)
    print("Correct Answer:", correct_answer)
    print("Wrong Answers:", wrong_answers)


    return render_template('subtraction.html', equation=equation, correct_answer=correct_answer, wrong_answers=wrong_answers, generate_subtraction=generate_subtraction(), score=0)


@app.route('/equations/multiplication')
def equations_multiplication():

    def generate_multiplication():
        operator = '*'
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        equation = str(num1) + operator + str(num2)
        correct_answer = eval(equation)
        wrong_answers = [correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10)]
        return equation, correct_answer, wrong_answers

    equation, correct_answer, wrong_answers = generate_multiplication()
    print("Equation:", equation)
    print("Correct Answer:", correct_answer)
    print("Wrong Answers:", wrong_answers)


    return render_template('multiplication.html', equation=equation, correct_answer=correct_answer, wrong_answers=wrong_answers, generate_multiplication=generate_multiplication(), score=0)



@app.route('/equations/division')
def equations_division():

    def generate_division():
        operator = '/'
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        equation = str(num1) + operator + str(num2)
        correct_answer = eval(equation)
        wrong_answers = [correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10),
                        correct_answer + random.randint(1, 10)]
        return equation, correct_answer, wrong_answers

    equation, correct_answer, wrong_answers = generate_division()
    print("Equation:", equation)
    print("Correct Answer:", correct_answer)
    print("Wrong Answers:", wrong_answers)


    return render_template('division.html', equation=equation, correct_answer=correct_answer, wrong_answers=wrong_answers, generate_division=generate_division(), score=0)



@app.route('/scores')
def scores():
    return 'These are your scores!'


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Submitted and Validated!')
        
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
        
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
        
        if check_user:            
            flash('A user with that email and/or username already exists.', 'danger')
            return redirect(url_for('signup'))

        new_user = User(email=email, username=username, password=password)


        flash(f'Thank you {new_user.username} for signing up!', 'success')
        
        # Redirect back to Home
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        print(username, password)

        user = User.query.filter_by(username=username).first()

        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user.username} is now logged in", "success")
            return redirect(url_for('index'))
        else:
            flash("Incorrect username and/or password. Please try again. If you do not have an account please visit the Sign Up page.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "warning")
    return redirect(url_for('index'))
