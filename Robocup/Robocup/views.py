"""
Routes and views for the flask application.
"""
# v.02.3 (21 57) 
#import sqlite3
from datetime import datetime
from json import JSONDecodeError
import json
import os

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask import Markup
from flask import render_template, redirect, request
from flask.ext.wtf import Form
from flask_wtf.file import FileField, FileRequired
from flask import send_from_directory
from wtforms import TextField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required
from wtforms.fields import StringField
from wtforms.widgets import TextArea
from wtforms import validators
from wtforms.fields.html5 import EmailField
# from wtforms.validators import ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required
import transliterate
from team_class import Team
from em import Sender
from RenderEvents import RenderEvent
from event import Event
from Robocup import app
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
    Password_input = TextField('Password_input', validators=[Required()])

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


CREATE_ALL_EVENTS = RenderEvent("events.json")
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(30),unique = True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
db.create_all()

@app.route('/')
@app.route('/home')
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

@app.route('/contact')
def contact():
    """Renders the contact page."""    
    return render_template('contact.html',
                           title='Contact', 
                           year=datetime.now().year,
                           message='Your contact page.',
                           )

@app.route('/russian_events')
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
     
@app.route('/regional_events')
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

@app.route('/international_events')
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
      

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
                           title='About',
                           year=datetime.now().year,
                           message='Your application description page.')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminAuth()
    if form.validate_on_submit():
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM Admins")
 
        rows = cur.fetchall()
       # print(len(rows))

        if rows[0][0] == form.Login_input.data and rows[0][1] == form.Password_input.data:
            user = User.query.filter_by(username='Admin').first()  
            login_user(user)
            print("SUPERUSER JOINED CHAT")
            
            return redirect('/admin_panel')
    return render_template('admin_auth.html',
                           title='About',
                           year=datetime.now().year,
                           message='Your application description page.',
                           form=form,
                           )

@app.route('/event_generator', methods=['GET', 'POST'])
@login_required
def event_generator():
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
        CREATE_ALL_EVENTS.save_new_event(new_event.make_event(),
                                                 new_event.name, save_to_json)
        return redirect('/')
    return render_template('admin.html',
                           title='About',
                           year=datetime.now().year,
                           message='Your application description page.',
                           form=form)
       
@app.route('/event_fix/<name>', methods=['GET', 'POST'])
@login_required
def event_fix(name=None):
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


@app.route('/error')
def error():
    """Renders the about page."""
    return render_template('Error.html',
                           title='Error',
                           year=datetime.now().year,
                           message='Dead.')


@app.route('/login/<name>', methods=['GET', 'POST'])
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

@app.route('/archive')
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


@app.route('/event_calendar')
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

@app.route('/admin_event_calendar', methods=['GET', 'POST'])
@login_required
def admin_event_calendar():
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

@app.route('/export_xlsx_teams', methods=['GET', 'POST'])
@login_required
def dump_teams():
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


@app.route('/export_xlsx_events', methods=['GET', 'POST']) 
@login_required
def dump_events():
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


@app.route('/humanoid')
def humanoid():
    return render_template('humanoid.html', 
                           title='Humanoid league'
                           ) 

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(401)
def not_authorized(error):
    return redirect('/admin')

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/admin_panel')
@login_required
def admin_panel():
    return render_template('admin_panel.html', 
        title='Admin panel'
                          )
