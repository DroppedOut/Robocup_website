"""
Routes and views for the flask application.
"""
#import sqlite3
# test comment to git
from datetime import datetime
from json import JSONDecodeError
import os

from flask import Markup
from flask import render_template, redirect
from flask.ext.wtf import Form
from flask_wtf.file import FileField, FileRequired
from wtforms import TextField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required
# from wtforms.validators import ValidationError

import transliterate
from team_class import Team
from em import Sender
from RenderEvents import RenderEvent
from event import Event
from Robocup import app
# import database 
class LoginForm(Form):
    """ LOGIN FORM CLASS """
    TeamName = TextField('TeamName', validators=[Required()])
    FirstMember = TextField('FirstMember', validators=[Required()])
    SecondMember = TextField('SecondMember', validators=[Required()])
    ThirdMember = TextField('ThirdMember',)
    ForthMember = TextField('ForthMember',)
    Mentor = TextField('Mentor',)
    League = SelectField('League', coerce=str, choices=[# cast val as int
        ('RobocupJuniorRescue Line', 'RobocupJuniorRescue Line'),
        ('RobocupJuniorRescue Maze', 'RobocupJuniorRescue Maze'),
        ('RobocupJuniorRescue OnStage', 'RobocupJuniorRescue OnStage'),
        ('RobocupJuniorRescue CoSpace', 'RobocupJuniorRescue CoSpace'),
        ('RobocupRescue Maze', 'RobocupRescue Maze'),
        ('Robocup@home', 'Robocup@home'),
        ('Robocup@WorkIndustrial', 'Robocup@WorkIndustrial'),])
    AttachFile = FileField('AttachFile', validators=[FileRequired()])

class AdminForm(Form):
    """ ADMIN FORM CLASS"""
    EventName = TextField('EventName', validators=[Required()])
    Status = SelectField('Status', validators=[Required()], coerce=str, choices=[
        ('Regional', 'Региональный'),
        ('Russian', 'Всероссийское'),
        ('International', 'Международное'),
        ])
    Sity = TextField('Sity', validators=[Required()])
    Description = TextField('Descriptoin', validators=[Required()])
    Country = TextField('Country')
    Date = DateField('Date', validators=[Required()])
CREATE_RUSSIAN_EVENTS = RenderEvent("russian_events.json")
CREATE_REGIONAL_EVENTS = RenderEvent("regional_events.json")
CREATE_INTERNATIONAL_EVENTS = RenderEvent("international_events.json")
CREATE_ALL_EVENTS = RenderEvent("russian_events.json","regional_events.json","international_events.json")
NEW_RUSSIAN_EVENTS = CREATE_RUSSIAN_EVENTS.get_render_events()
NEW_REGIONAL_EVENTS = CREATE_REGIONAL_EVENTS.get_render_events()
NEW_INTERNATIONAL_EVENTS = CREATE_INTERNATIONAL_EVENTS.get_render_events()
NEW_ALL_EVENTS = CREATE_ALL_EVENTS.get_render_events()
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    try:
        CREATE_ALL_EVENTS.update_all("russian_events.json","regional_events.json","international_events.json")
        events = CREATE_ALL_EVENTS.get_render_events()
        print(events)
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
        CREATE_RUSSIAN_EVENTS.update("russian_events.json")
        new_events = CREATE_RUSSIAN_EVENTS.get_render_events()
        print(new_events)
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
def regioanl_events():
    """Renders the about page."""
    try:
        CREATE_RUSSIAN_EVENTS.update("regional_events.json")
        new_events = CREATE_RUSSIAN_EVENTS.get_render_events()
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
        CREATE_RUSSIAN_EVENTS.update("international_events.json")
        new_events = CREATE_RUSSIAN_EVENTS.get_render_events()
        print(new_events)
 
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
        print(form.Status.data)
        new_event.sity = form.Sity.data
        new_event.date = form.Date.data
        new_event.desc = form.Description.data
        save_to_json = ""
        if new_event.status == 'Russian':
            save_to_json = "russian_events.json"
            CREATE_RUSSIAN_EVENTS.save_new_event(new_event.make_event(),
                                                 new_event.name, save_to_json)
        if new_event.status == 'International':
            save_to_json = "international_events.json" 
            CREATE_INTERNATIONAL_EVENTS.save_new_event(new_event.make_event(),
                                                       new_event.name, save_to_json)            
        if new_event.status == 'Regional':
            save_to_json = "regional_events.json"  
            CREATE_REGIONAL_EVENTS.save_new_event(new_event.make_event(),
                                                  new_event.name, save_to_json)
        #events = create_events.get_render_events()
        return redirect('/')
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders registration page"""
    form = LoginForm()
    if form.validate_on_submit():
       
        filename = form.AttachFile.data.filename
        try:
            transliterate.translit(filename, reversed=True)
        except transliterate.exceptions.LanguageDetectionError:
            filename = form.AttachFile.data.filename
        form.AttachFile.data.save('upload/' + filename)
        print(filename)
        print(len(filename))
        team = Team(form.TeamName.data, form.FirstMember.data, form.SecondMember.data,
                    form.ThirdMember.data, form.ForthMember.data, form.Mentor.data, 
                    form.League.data)

        team.insert()
        team.get_text()
        team.write()
        sender = Sender
        sender.send_letter(sender, 'upload/' + filename, team.text)
            #team.kek()
    return render_template('register.html', 
                           title='Sign In',
                           form=form)
@app.route('/event_calendar')
def event_calendar():
   return render_template('event_calendar.html',
                           title='Error',
                           year=datetime.now().year,
                           message='Dead.')