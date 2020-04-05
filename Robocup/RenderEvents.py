import json
import io
import random
from collections import OrderedDict
from datetime import datetime
#import os
class RenderEvent:

    def __init__(self, json_file1,json_file2=".",json_file3="."):
        self.events = [] 
        self.render_events = []
        self.data = {}
        if json_file2==".":
            with open(json_file1, "r", encoding='utf-8') as read_file:
                try:
                    with open(json_file1, "r",encoding='utf-8') as read_file1:
                        self.data = dict(list(json.load(read_file1).items())+list(self.data.items()))
                    with open(json_file2, "r",encoding='utf-8') as read_file2:
                        self.data = dict(list(json.load(read_file2).items())+list(self.data.items()))
                    with open(json_file3, "r",encoding='utf-8') as read_file3:
                        self.data = dict(list(json.load(read_file3).items())+list(self.data.items()))
                    index = -1
                    for key in self.data:
                       
                        index += 1
                        self.events.append([])
                        for k in self.data[key]:
                            self.events[index].append(str(self.data[key][k]))
                    for i in range(len(self.events)):
                        self.render_events.append("".join(self.events[i]))
                        self.render_events[i] = '''<div class="col-md-4"> ''' + self.render_events[i] + \
                                            '''<p><a class="btn btn-default" href="/login"> 
                                            Зарегестрироваться &raquo;</a></p> </div>'''
                except:
                    self.data = {}
                    print("feels bad man")
        else:
            with open(json_file1, "r", encoding='utf-8') as read_file1:
                with open(json_file2, "r", encoding='utf-8') as read_file2:
                    with open(json_file3, "r", encoding='utf-8') as read_file3:
                        try:
                            self.data = json.load(read_file)
                            index = -1
                            for key in self.data:
                       
                                index += 1
                                self.events.append([])
                                for k in self.data[key]:
                                    self.events[index].append(str(self.data[key][k]))
                            for i in range(len(self.events)):
                                self.render_events.append("".join(self.events[i]))
                                self.render_events[i] = '''<div class="col-md-4"> ''' + self.render_events[i] + \
                                            '''<p><a class="btn btn-default" href="/login"> 
                                            Зарегестрироваться &raquo;</a></p> </div>'''
                        except:
                            self.data = {}
                            print("feels bad man")

               
    def update(self, json_file):

        self.events.clear()
        self.render_events.clear()
        with open(json_file, "r",encoding='utf-8') as read_file:
            self.data = json.load(read_file)
            sorted_events = OrderedDict(self.data)
            self.data = dict(OrderedDict(sorted(sorted_events.items(), key=lambda t: int(t[1]["date"][15:17])+int(t[1]["date"][18:20])*30+int(t[1]["date"][21:25])*365)))
            #sort 
            print (self.data)
            #print(self.data)
            index = -1
            for key in self.data:
               print (self.data[key]['date'])        
               index+=1
               self.events.append([])
               for k in self.data[key]:
                    self.events[index].append(str(self.data[key][k]))
                    
            for i in range(len(self.events)):
                self.render_events.append("".join(self.events[i]))
                self.render_events[i] = '''<div class="col-md-4"> ''' + self.render_events[i] + \
                                        '''<p><a class="btn btn-default" href="/login"> 
                                        Зарегестрироваться &raquo;</a></p> </div>'''

    def save_new_event(self, new_event, event_name, json_file):
        with open(json_file, "w", encoding="utf-8") as file:
            self.data[event_name + str(random.randint(0,4214231312))] = new_event
         
            json.dump(self.data, file)
    def get_render_events(self):
        return self.render_events

    def update_all(self, json_file1,json_file2,json_file3):
        self.events.clear()
        self.render_events.clear()
        with open(json_file1, "r",encoding='utf-8') as read_file1:
            self.data = dict(list(json.load(read_file1).items())+list(self.data.items()))
        with open(json_file2, "r",encoding='utf-8') as read_file2:
            self.data = dict(list(json.load(read_file2).items())+list(self.data.items()))
        with open(json_file3, "r",encoding='utf-8') as read_file3:
            self.data = dict(list(json.load(read_file3).items())+list(self.data.items()))
        sortkey=datetime.now().year*365+datetime.now().month*30+datetime.now().day
        sorted_events = OrderedDict(self.data)
        self.data = dict(OrderedDict(sorted(sorted_events.items(), key=lambda t: int(t[1]["date"][15:17])+int(t[1]["date"][18:20])*30+int(t[1]["date"][21:25])*365-sortkey)))
        #sort 
        index = -1
        for key in self.data:
            dt = int(self.data[key]["date"][15:17])+int(self.data[key]["date"][18:20])*30+int(self.data[key]["date"][21:25])*365
            index+=1
            self.events.append([])
            if dt>sortkey:
                for k in self.data[key]:
                    self.events[index].append(str(self.data[key][k]))
                    
        for i in range(len(self.events)):
            self.render_events.append("".join(self.events[i]))
            if len(self.events[i]) != 0:
                self.render_events[i] = '''<div class="col-md-4"> ''' + self.render_events[i] + \
                                        '''<p><a class="btn btn-default" href="/login"> 
                                        Зарегестрироваться &raquo;</a></p> </div>'''
            else:
                self.render_events[i] = ''

            
