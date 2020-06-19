"""
Routes and views for the flask application.
"""
# v.02.3 (21 57) 
#import sqlite3

#to do :
#    fix 401 error
#    add refree cabinet
#
from datetime import datetime
from json import JSONDecodeError
import json
import os
from copy import deepcopy
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask import Markup
from flask import render_template, redirect, request
from flask.ext.wtf import Form
from flask_wtf.file import FileField, FileRequired
from flask import send_from_directory
from wtforms import TextField, SelectField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required
from wtforms.fields import StringField
from wtforms.widgets import TextArea
from wtforms import validators
from wtforms.fields.html5 import EmailField
# from wtforms.validators import ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user ,logout_user
import transliterate
from team_class import Team
from em import Sender
from RenderEvents import RenderEvent
from event import Event
from Robocup import application
import database 
import sqlite3
import pandas as pd
import qrcode
import random
import string
class LoginForm(Form):
    """ LOGIN FORM CLASS """
    TeamName = TextField('TeamName', validators=[Required()])
    FirstMember = TextField('FirstMember', validators=[Required()])
    SecondMember = TextField('SecondMember', validators=[Required()])
    ThirdMember = TextField('ThirdMember',)
    ForthMember = TextField('ForthMember',)
    Mentor = TextField('Mentor',)
    Email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    League = SelectField('League', coerce=str, choices=[# cast val as int
        ('RobocupJuniorRescue Line', 'RobocupJuniorRescue Line'),
        ('RobocupJuniorRescue Maze', 'RobocupJuniorRescue Maze'),
        ('RobocupJuniorRescue OnStage', 'RobocupJuniorRescue OnStage'),
        ('RobocupJuniorRescue CoSpace', 'RobocupJuniorRescue CoSpace'),
        ('RobocupRescue Maze', 'RobocupRescue Maze'),
        ('Robocup@home', 'Robocup@home'),
        ('Robocup@WorkIndustrial', 'Robocup@WorkIndustrial')])
    AttachFile = FileField('AttachFile', validators=[FileRequired()])
class RefreeForm(Form):
    Login = TextField('Login', validators=[Required()])
    Email = TextField("Email",  [validators.Required("Please enter your email address."),
                                 validators.Email("Please enter your email address.")])
    Password = PasswordField('New Password', [
        validators.Required("please enter your password"),
        validators.EqualTo('Confirm', message='Passwords must match')
    ])
    Confirm = PasswordField('Repeat Password')
    FirstName = TextField('FirstName', validators=[Required()])
    SecondName = TextField('SecondName', validators=[Required()])
    League = SelectField('League', coerce=str, choices=[
        ('RobocupJuniorRescue Line', 'RobocupJuniorRescue Line'),
        ('RobocupJuniorRescue Maze', 'RobocupJuniorRescue Maze'),
        ('RobocupJuniorRescue OnStage', 'RobocupJuniorRescue OnStage'),
        ('RobocupJuniorRescue CoSpace', 'RobocupJuniorRescue CoSpace'),
        ('RobocupRescue Maze', 'RobocupRescue Maze'),
        ('Robocup@home', 'Robocup@home'),
        ('Robocup@WorkIndustrial', 'Robocup@WorkIndustrial')])

class AdminForm(Form):
    """ ADMIN FORM CLASS"""
    EventName = TextField('EventName', validators=[Required()])
    Status = SelectField('Status', validators=[Required()], coerce=str, choices=[
        ('Regional', 'Региональный'),
        ('Russian', 'Всероссийское'),
        ('International', 'Международное'),
        ])
    City = TextField('City', validators=[Required()])
    Adress = TextField('Addr', validators=[Required()])
    Country = TextField('Country')
    Date = DateField('Date', validators=[Required()])
    Desc = StringField(u'Text', widget=TextArea(),validators=[Required()])

class AdminAuth(Form):
    """class for admin auth."""
    Login_input = TextField('Login_input', validators=[Required()])
    Password_input = PasswordField('Password_input', validators=[Required()])

class Dump_teams_form(Form):
     League = SelectField('League', coerce=str, choices=[
        ('RobocupJuniorRescue Line', 'RobocupJuniorRescue Line'),
        ('RobocupJuniorRescue Maze', 'RobocupJuniorRescue Maze'),
        ('RobocupJuniorRescue OnStage', 'RobocupJuniorRescue OnStage'),
        ('RobocupJuniorRescue CoSpace', 'RobocupJuniorRescue CoSpace'),
        ('RobocupRescue Maze', 'RobocupRescue Maze'),
        ('Robocup@home', 'Robocup@home'),
        ('Robocup@WorkIndustrial', 'Robocup@WorkIndustrial'),
        ('*', 'Скачать все')])

class Dump_events_Form(Form):
     Rank = SelectField('Rank', coerce=str, choices=[
        ('Regional', 'Региональныее мероприятия'),
        ('Russian', 'Всероссийские мероприятия'),
        ('International', 'Международные мероприятия'),
        ('archive_events', 'Прошедшие мероприятия')])
class RefreeAuthForm(Form):
    Login = TextField('Login_input', validators=[Required()])
    Password = PasswordField('New Password', [
        validators.Required("please enter your password")
        
    ])
class Refree:
    def __init__(self, name, secondName, email, league):
        self.name = name
        self.secondName = secondName
        self.email = email
        self.league = league

CREATE_ALL_EVENTS = RenderEvent("events.json")
SECRET_KEY = os.urandom(32)
application.config['SECRET_KEY'] = SECRET_KEY
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
db = SQLAlchemy(application)
login_manager = LoginManager()
login_manager.init_app(application)
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(30),unique = True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
db.create_all()

@application.route('/')
@application.route('/home')
def home():
    """Renders the home page."""
    try:
        CREATE_ALL_EVENTS.update("events.json",'*')
        events = CREATE_ALL_EVENTS.get_render_events()
        #print(events)
         #i really don't know why it doesn't work with normal for
        for i, _ in enumerate(events): 
            events[i] = Markup(events[i])
    except JSONDecodeError:
        events = []
    return render_template('index.html',
                           title='Home Page',
                           year=datetime.now().year,
                           event=events)

@application.route('/contact')
def contact():
    """Renders the contact page."""    
    return render_template('contact.html',
                           title='Contact', 
                           year=datetime.now().year,
                           message='Your contact page.',
                           )

@application.route('/russian_events')
def russian_events():
    """Renders the about page."""
    try:
        CREATE_ALL_EVENTS.update("events.json",'Russian')
        new_events =  CREATE_ALL_EVENTS.get_render_events()
        # print(new_events)
        # i really don't know why it doesn't work with normal for
        for i, _ in enumerate(new_events): 
            new_events[i] = Markup(new_events[i])
    except JSONDecodeError:
        new_events = []
    return render_template('russian_events.html',
                           title='Events',
                           year=datetime.now().year,
                           message='Your application description page.',
                           event=new_events)
     
@application.route('/regional_events')
def regional_events():
    """Renders the about page."""
    try:
        CREATE_ALL_EVENTS.update("events.json",'Regional')
        new_events =  CREATE_ALL_EVENTS.get_render_events()
       # print (new_events)
 
        for i, _ in enumerate(new_events):
            new_events[i] = Markup(new_events[i])
    except JSONDecodeError:
        new_events = []
    return render_template('regional_events.html',
                           title='Events',
                           year=datetime.now().year,
                           message='Your application description page.',
                           event=new_events
       )

@application.route('/international_events')
def international_events():
    """Renders the about page."""
    try:
        CREATE_ALL_EVENTS.update("events.json",'International')
        new_events =  CREATE_ALL_EVENTS.get_render_events()
        # print(new_events)
 
        for i, _ in enumerate(new_events):
            new_events[i] = Markup(new_events[i])
    except JSONDecodeError:
        new_events = []
    return render_template('international_events.html',
                           title='Events',
                           year=datetime.now().year,
                           message='Your application description page.',
                           event=new_events
                           )
      

@application.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
                           title='About',
                           year=datetime.now().year,
                           message='Your application description page.')

@application.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminAuth()
    if form.validate_on_submit():
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM Admins")
 
        rows = cur.fetchall()
       # print(len(rows))

        if rows[0][0] == form.Login_input.data and rows[0][1] == form.Password_input.data:
            logout_user()
            user = User.query.filter_by(username='Admin').first()  
            login_user(user)
            print("SUPERUSER JOINED CHAT")
            print(current_user.username)
            
            return redirect('/admin_panel')
    return render_template('admin_auth.html',
                           title='About',
                           year=datetime.now().year,
                           message='Your application description page.',
                           form=form,
                           )

@application.route('/event_generator', methods=['GET', 'POST'])
@login_required
def event_generator():
    """Renders the about page."""
    if current_user.username!='Admin':
        return redirect('/')
    form = AdminForm()
    new_event = Event()


    if form.validate_on_submit():

        new_event.name = form.EventName.data
        new_event.status = form.Status.data
        if new_event.status == 'Russian':
            new_event.country = 'Россия'

        else:
            new_event.country = form.Country.data

        # print(form.Status.data)
        new_event.city = form.City.data
        new_event.date = form.Date.data
        new_event.desc = form.Desc.data
        new_event.adress = form.Adress.data

        save_to_json = "events.json"
        CREATE_ALL_EVENTS.save_new_event(new_event.make_event(),
                                                 new_event.name, save_to_json)
        return redirect('/')
    return render_template('admin.html',
                           title='About',
                           year=datetime.now().year,
                           message='Your application description page.',
                           form=form)
       
@application.route('/event_fix/<name>', methods=['GET', 'POST'])
@login_required
def event_fix(name=None):
    if current_user.username!='Admin':
        return redirect('/')
    """Renders the about page."""
    form = AdminForm()
    new_event = Event()


    if form.validate_on_submit():

        new_event.name = form.EventName.data
        new_event.status = form.Status.data
        if new_event.status == 'Russian':
            new_event.country = 'Россия'

        else:
            new_event.country = form.Country.data

        # print(form.Status.data)
        new_event.city = form.City.data
        new_event.date = form.Date.data
        new_event.desc = form.Desc.data
        new_event.adress = form.Adress.data

        save_to_json = "events.json"
        CREATE_ALL_EVENTS.update_event(new_event.make_event(),
                                                 name, save_to_json)
        return redirect('/')
    event = CREATE_ALL_EVENTS.get_existing_event(name,"events.json")
    form.EventName.data=event['name']
    form.Status.data=event['status']
    form.Country.data=event['country']
    form.City.data=event['city']
    form.Desc.data = event['desc']
    form.Adress.data=event['adress']
    #form.Date.data=event['date'] //FUCK STRING DATES
    return render_template('admin.html',
                           title='About',
                           year=datetime.now().year,
                           message='Your application description page.',
                           form=form)


@application.route('/error')
def error():
    """Renders the about page."""
    return render_template('Error.html',
                           title='Error',
                           year=datetime.now().year,
                           message='Dead.')


@application.route('/login/<name>', methods=['GET', 'POST'])
def login(name=None):
    """Renders registration page"""
    form = LoginForm()
    if form.validate_on_submit():
       
        filename = form.AttachFile.data.filename
        try:
            filename = transliterate.translit(filename, reversed=True)
        except transliterate.exceptions.LanguageDetectionError:
            filename = form.AttachFile.data.filename
        form.AttachFile.data.save('upload/' + filename)

        team = Team(form.TeamName.data, form.FirstMember.data, form.SecondMember.data,
                    form.ThirdMember.data, form.ForthMember.data, form.Mentor.data, 
                    form.League.data,name)
       
       # qr_code = None
        team.insert()
        team.get_text()
        team.write()
        qr_code = qrcode.make(team.text)
        print("qr sucseed")
        letters = string.ascii_lowercase
        qr_code_fn = "qr/"
        qr_code_fn += ''.join(random.choice(letters) for i in range(10))
        qr_code_fn +=form.TeamName.data + ".png"
        qr_code.save(qr_code_fn)
        sender = Sender
        #send qr
        sender.send_qr(sender, qr_code_fn, form.Email.data, "Registration qr code" )
        print("qr sended")
        sender.send_letter(sender, 'upload/' + filename, team.text)
        print("sended info")
        return redirect('/')
    return render_template('register.html', 
                           title='Sign In',
                           form=form)

@application.route('/archive')
def archive():
    try:
        CREATE_ALL_EVENTS.update("archive_events.json",'*')
        archive_events = CREATE_ALL_EVENTS.get_render_events()
        for i, _ in enumerate(archive_events):
            archive_events[i] = Markup(archive_events[i])
    except JSONDecodeError:
        archive_events = []
    return render_template('archive.html',
                           title='Archive',
                           event=archive_events
                           )


@application.route('/event_calendar')
def event_calendar():
    try:
        CREATE_ALL_EVENTS.update("events.json",'International')
        new_int_events = CREATE_ALL_EVENTS.get_render_events()
       
         #i really don't know why it doesn't work with normal for
        for i, _ in enumerate(new_int_events): 
            new_int_events[i] = Markup(new_int_events[i])
    except JSONDecodeError:
        new_int_events = []
    try:
        CREATE_ALL_EVENTS.update("events.json",'Regional')
        new_reg_events = CREATE_ALL_EVENTS.get_render_events()
        
         #i really don't know why it doesn't work with normal for
        for i, _ in enumerate(new_reg_events): 
            new_reg_events[i] = Markup(new_reg_events[i])
    except JSONDecodeError:
        new_reg_events = []
    try:
        CREATE_ALL_EVENTS.update("events.json",'Russian')
        new_rus_events = CREATE_ALL_EVENTS.get_render_events()
        
         #i really don't know why it doesn't work with normal for
        for i, _ in enumerate(new_rus_events): 
            new_rus_events[i] = Markup(new_rus_events[i])
    except JSONDecodeError:
        new_rus_events = []
    return render_template('event_calendar.html',
                           title='Error',
                           year=datetime.now().year,
                           message='Dead.',
                           reg_events = new_reg_events,
                           int_events = new_int_events,
                           rus_events = new_rus_events
                           )

@application.route('/admin_event_calendar', methods=['GET', 'POST'])
@login_required
def admin_event_calendar():
    if current_user.username!='Admin':
        return redirect('/')
    form=Form()
    if request.method == 'POST':
        names_list=CREATE_ALL_EVENTS.get_event_names('*',"events.json")
        for item in names_list:
            if str('r'+item) in request.form:
                CREATE_ALL_EVENTS.destroy_event(item,"events.json")
            elif str(item) in request.form:
                return redirect('/event_fix/'+item)

    try:
        CREATE_ALL_EVENTS.admin_update("events.json",'International')
        new_int_events = CREATE_ALL_EVENTS.get_render_events()
       
         #i really don't know why it doesn't work with normal for
        for i, _ in enumerate(new_int_events): 
            new_int_events[i] = Markup(new_int_events[i])
    except JSONDecodeError:
        new_int_events = []
    try:
        CREATE_ALL_EVENTS.admin_update("events.json",'Regional')
        new_reg_events = CREATE_ALL_EVENTS.get_render_events()
        
         #i really don't know why it doesn't work with normal for
        for i, _ in enumerate(new_reg_events): 
            new_reg_events[i] = Markup(new_reg_events[i])
    except JSONDecodeError:
        new_reg_events = []
    try:
        CREATE_ALL_EVENTS.admin_update("events.json",'Russian')
        new_rus_events = CREATE_ALL_EVENTS.get_render_events()
        
         #i really don't know why it doesn't work with normal for
        for i, _ in enumerate(new_rus_events): 
            new_rus_events[i] = Markup(new_rus_events[i])
    except JSONDecodeError:
        new_rus_events = []
    return render_template('event_calendar.html',
                           title='Error',
                           year=datetime.now().year,
                           message='Dead.',
                           reg_events = new_reg_events,
                           int_events = new_int_events,
                           rus_events = new_rus_events)

@application.route('/export_xlsx_teams', methods=['GET', 'POST'])
@login_required
def dump_teams():
    if current_user.username!='Admin':
        return redirect('/')
    form = Dump_teams_form()
    flag=False
    if form.validate_on_submit():
        conn = sqlite3.connect("data.db")
        if form.League.data !='*':
            df = pd.read_sql('select * from teams where league= '+str('"')+form.League.data+str('"'), conn)
        else:
            df = pd.read_sql('select * from teams', conn)
        if df.empty:  
            flag=True
        else:
            if form.League.data !='*':
                df.to_excel(r'Robocup/downloads/'+form.League.data+'.xlsx', index=False)
            else:
                df.to_excel(r'Robocup/downloads/All.xlsx', index=False)
                return send_from_directory('downloads\\', 'All.xlsx',as_attachment=True)
            return send_from_directory('downloads\\', form.League.data+'.xlsx',as_attachment=True)
    return render_template('export_teams_xlsx.html', 
                           title='Выгрузка',
                           form=form,flag=flag)


@application.route('/export_xlsx_events', methods=['GET', 'POST']) 
@login_required
def dump_events():
    if current_user.username!='Admin':
        return redirect('/')
    form = Dump_events_Form()
    flag=False
    if form.validate_on_submit():
        if form.Rank.data != 'archive_events':
            data=CREATE_ALL_EVENTS.get_pure_events(form.Rank.data,"events.json")
        else:
            with open(form.Rank.data+'.json') as data_file: 
                data = json.load(data_file)
        df = pd.DataFrame(data)
        if df.empty:  
            flag=True
        else:
            df.to_excel("Robocup/downloads/"+form.Rank.data+'.xlsx')
            return send_from_directory('downloads\\', form.Rank.data+'.xlsx',as_attachment=True)
    return render_template('export_events_xlsx.html', 
                           title='Выгрузка',
                           form=form,flag=flag)


@application.route('/humanoid')
def humanoid():
    return render_template('humanoid.html', 
                           title='Humanoid league'
                           ) 

@application.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@application.errorhandler(401)
def not_authorized(error):
    # fix this
    return redirect('/admin')

@application.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@application.route('/admin_panel')
@login_required
def admin_panel():
    if current_user.username != 'Admin':
        return redirect('/')
    return render_template('admin_panel.html', 
        title='Admin panel'
                          )
@application.route('/refree_register', methods=['GET', 'POST'])
def refree_register():
    form = RefreeForm()
    if form.validate_on_submit():
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        
        
        query = "INSERT INTO refrees VALUES(?,?,?,?,?,?,?)"
        cur.execute(query, (form.Login.data, form.Email.data, form.Password.data ,
                            form.FirstName.data, form.SecondName.data, form.League.data," "))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('refree_register.html', 
        title='Admin panel',
        form = form   )
@application.route('/refree_auth', methods=['GET', 'POST'])
def refree_auth():
    form = RefreeAuthForm()
    if form.validate_on_submit():
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM refrees")
        rows = cur.fetchall()
       # print(rows)
        for i in rows:
            if i[0] == form.Login.data  or i[1] == form.Login.data and i[2] == form.Password.data:
                print("found!")
                print(form.Login.data)
                print(form.Password.data)
                print(i[0],i[1],i[3])
                logout_user()
                try:

                    User.query.delete()
                    db.session.commit()
                except:
                    pass

                cu = User(username = form.Login.data)
                ab = User(username = 'Admin')
                db.session.add(cu)
                db.session.commit()
                db.session.add(ab)
                db.session.commit()
                user = User.query.filter_by(username=form.Login.data).first()  
                login_user(user)
                return redirect('/')
            else:
                print("go away")
    return render_template('refree_auth.html', 
        title='Admin panel',
        form = form   )
class league_select(Form):
     League = SelectField('League', coerce=str,validators= [Required()], choices=[
        ('RobocupJuniorRescue Line', 'RobocupJuniorRescue Line'),
        ('RobocupJuniorRescue Maze', 'RobocupJuniorRescue Maze'),
        ('RobocupJuniorRescue OnStage', 'RobocupJuniorRescue OnStage'),
        ('RobocupJuniorRescue CoSpace', 'RobocupJuniorRescue CoSpace'),
        ('RobocupRescue Maze', 'RobocupRescue Maze'),
        ('Robocup@home', 'Robocup@home'),
        ('Robocup@WorkIndustrial', 'Robocup@WorkIndustrial'),
        ])
@application.route('/refree_cabinet', methods=['GET', 'POST'])
#@login_required

def refree_cabinet():
    # '/refree_cabinet/<name>'
    #usr = current_user.username
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM refrees WHERE login = ?", ('Test1',))
    rows = cur.fetchall()
    print(rows)
    form = RefreeForm()
    form.League.data = deepcopy(rows[0][5]) # присвоить значение из бд
    refree = Refree(rows[0][3],rows[0][4],rows[0][1],rows[0][5])
    if request.method == 'POST':
        #форма не работает нормально
        cur.execute("UPDATE refrees SET league = ? WHERE login = ?", (form.League.data, 'Test1',)) # обновить бд
        print(form.League.data)
        conn.commit()
        #form.League.data = rows[0][5]
        return redirect('/refree_cabinet')
       # UPDATE table
#SET column_1 = new_value_1,
    #column_2 = new_value_2
#WHERE
    return render_template('refree_cabinet.html', 
        title='Admin panel',
        form = form,
        refree = refree
        )
