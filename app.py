from flask import Flask, render_template,flash,url_for,redirect,request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, UserMixin, RoleMixin, login_required, SQLAlchemyUserDatastore, hash_password, current_user,roles_required
from flask_mailman import Mail
import config
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
Bootstrap5(app)

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                       )
                       

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255), unique=True)
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    webauth = db.relationship('WebAuth', backref='user', uselist=False)

class WebAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    teacher = db.relationship('User' , backref='course_taught')
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', backref='enrollment')
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student = db.relationship('User', backref='enrollment')
    grade = db.Column(db.Float(40) ,nullable=True)

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Admin', 'Admin')])
    submit = SubmitField('Register')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')
        
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
mail = Mail(app)

@app.route('/')
@login_required
def index():
    courses_count = Course.query.count()
    students_count = User.query.join(User.roles).filter(Role.name == 'Student').count()
    teachers_count = User.query.join(User.roles).filter(Role.name == 'Teacher').count()
    return render_template('index.html', courses_count=courses_count, students_count=students_count, teachers_count=teachers_count, title='Dashboard')
 
@app.route('/courses')
@login_required
def courses():
    if current_user.has_role('Admin') or current_user.has_role('Teacher'):
        courses = Course.query.all()
    else:
        courses = Course.query.all()
    return render_template('courses.html', title='Courses | SMS', courses=courses)
    
       

@app.route('/courses/<int:course_id>')
@login_required
def course_details(course_id):
    course = Course.query.get_or_404(course_id)
    # enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    return render_template('course_details.html', title='Course Details | SMS',course=course,course_id=course_id)#, enrollments=enrollments)
 

# @app.route('/manage_courses/<int:course_id>', methods=['GET'])
# @roles_required('Teacher')
# def manage_courses(course_id):
 # if current_user.has_role('Teacher'):
        #     courses = Course.query.filter_by(teacher_id=current_user.id).all()
        # else:
        #     courses = Course.query.all()
#     course = Course.query.get_or_404(course_id)
#     enrollments = Enrollment.query.filter_by(course_id=course_id).all()
#     students = [enrollment.student for enrollment in enrollments]
#     return render_template('manage_courses.html', title='Manage Courses | SMS', course=course, enrollments=enrollments, students=students)


@app.route('/create_course',methods=['POST','GET'])
@roles_required('Admin')
def create_course():
    if request.method == 'POST':
        name = request.form.get('name')
        teacher_id = request.form.get('teacher_id')
        course = Course(name=name, teacher_id=teacher_id)
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully','success')
        return redirect(url_for('courses'))
    else:
        teachers = User.query.join(roles_users).join(User.roles).filter(Role.name == 'Teacher').all()
        return render_template('create_course.html', title='Create Course | SMS', teachers=teachers)




@app.route('/enroll/<int:course_id>', methods=['GET','POST'])
@roles_required('Student')
def enroll(course_id):
    course = Course.query.get_or_404(course_id)    
    if Enrollment.query.filter_by(student_id=current_user.id,course_id=course_id).first():
        flash('You are already enrolled in this course','warning')
        return redirect(url_for('courses'))
    else:
        enrollment = Enrollment(course_id=course_id, student_id=current_user.id)
        db.session.add(enrollment)
        db.session.commit()
        flash('Enrollment successful','success')
    return redirect(url_for('course_details',course=course))#check here

@app.route('/grade/<int:enrollment_id>', methods=['GET','POST'])
@roles_required('Teacher')
def grade(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    #Check if thr current user is the teacher of the course
    if enrollment.course.teacher_id != current_user.id:
        flash('You do not have permission to grade this course','warning')
        return redirect(url_for('courses'))
    if request.method == 'POST':
        grade = request.form.get('grade')
        if grade:
            try:
                grade_value = float(grade)
                if 0 <= grade_value <= 100:  # Example range check
                    enrollment.grade = grade_value
                    db.session.commit()
                    flash('Grade submitted successfully')
                else:
                    flash('Grade must be between 0 and 100')
            except ValueError:
                flash('Invalid grade value')
        else:
            flash('No grade provided')
    return redirect(url_for('courses', course=enrollment.course))


@app.route('/register_user',methods=['POST','GET'])
@roles_required('Admin')
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = form.role.data

        # Check if the user already exists
        if user_datastore.find_user(email=email):
            flash('Email is already registered','warning')
            return redirect(url_for('register_user'))

         # Find the role in the database
        role = user_datastore.find_role(role)
        if role is None:
            flash(f'Role "{role}" does not exist.', 'danger')
            return redirect(url_for('register_user'))
        
      # Hash the password and create the user
        hashed_password = hash_password(password)
        user = user_datastore.create_user(email=email, password=hashed_password)
        
        
        # Add role to user
        user_datastore.add_role_to_user(user,role)
        
        db.session.commit()
        flash('User registered successfully','success')
        return redirect(url_for('index'))
    
    return render_template('register_user.html', title='Register User | SMS', form=form) 
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        #Create roles
        user_datastore.find_or_create_role(name='Admin',description='Administrator')
        user_datastore.find_or_create_role(name='Teacher',description='Teacher')
        user_datastore.find_or_create_role(name='Student',description='Student')

        #Create Admin
        if not user_datastore.find_user(email='enockbett427@gmail.com'):
            hashed_password = hash_password('captain77')
            user_datastore.create_user(email='enockbett427@gmail.com',password=hashed_password,roles=[user_datastore.find_role('Admin')])
            db.session.commit()

        #Create teacher
        if not user_datastore.find_user(email='captainbett77@gmail.com'):
            hashed_password = hash_password('captain77')
            user_datastore.create_user(email='captainbett77@gmail.com',password=hashed_password,roles=[user_datastore.find_role('Teacher')])
            db.session.commit()

          #Create student
        if not user_datastore.find_user(email='aaronrop40@gmail.com'):
            hashed_password = hash_password('captain77')
            user_datastore.create_user(email='aaronrop40@gmail.com',password=hashed_password,roles=[user_datastore.find_role('Student')])
            db.session.commit()
        if not user_datastore.find_user(email='chelangatgladwel9@gmail.com'):
            hashed_password = hash_password('captain77')
            user_datastore.create_user(email='chelangatgladwel9@gmail.com',password=hashed_password,roles=[user_datastore.find_role('Student')])
            db.session.commit()

    
    app.run(debug=True)
 