import json
import io
import random
from collections import OrderedDict
from datetime import datetime
import os.path

class RenderEvent:

    def __init__(self, json_file1,json_file2=".",json_file3="."):
        self.events = [] 
        self.render_events = []
        self.data = {}
        if json_file2==".":
            if not os.path.exists(json_file1):
                with open(json_file1, "w",encoding='utf-8') as file:
                        json.dump(self.data,file)
            if not os.path.exists("archive_events.json"):
                with open("archive_events.json", "w",encoding='utf-8') as file:
                        json.dump(self.data,file)
            with open(json_file1, "r", encoding='utf-8') as read_file:
                try:
                    self.update_all(json_file1,json_file2,json_file3)
                except:
                    self.data = {}
                    print("feels bad man")
        else:
            if not os.path.exists(json_file1):
                with open(json_file1, "w",encoding='utf-8') as file:
                        json.dump(self.data,file)
            if not os.path.exists(json_file2):
                with open(json_file2, "w",encoding='utf-8') as file:
                        json.dump(self.data,file)
            if not os.path.exists(json_file3):
                with open(json_file3, "w",encoding='utf-8') as file:
                        json.dump(self.data,file)
            if not os.path.exists("archive_events.json"):
                with open("archive_events.json", "w",encoding='utf-8') as file:
                        json.dump(self.data,file)
            try:
                self.update(json_file1)
            except:
                self.data = {}
                print("feels bad man")

    def update(self, json_file):

        self.events.clear()
        self.render_events.clear()
        if json_file != "archive_events.json":
            self.check_outdated(json_file)
        with open(json_file, "r",encoding='utf-8') as read_file:
            self.data = json.load(read_file)
            sorted_events = OrderedDict(self.data)
            self.data = dict(OrderedDict(sorted(sorted_events.items(), key=lambda t: int(t[1]["date"][0:2])+int(t[1]["date"][3:5])*30+int(t[1]["date"][6:10])*365)))
            #sort 
            #print(self.data)
            index = -1
            for key in self.data:
               print (self.data[key]['date'])        
               index+=1
               self.events.append([])
               #for k in self.data[key]:
               self.events[index].append("<h2> " + str(self.data[key]['name']) + "<br><strong> " \
                     + str(self.data[key]['status']) + "</strong></h2>")
               self.events[index].append('<p> <li style="list-style-type: none;" > \
                     <a href="#" class="" style="padding: 0px" data-toggle="dropdown" role="button" \
                     aria-haspopup="true" aria-expanded="false"><strong>Инфо</strong> \
                     <span class="caret"></span></a> <ul class="dropdown-menu"> \
                  <li>'+ str(self.data[key]['desc']) +'</li></ul> </li>')
               self.events[index].append('<strong> Страна: </strong>' + str(self.data[key]['country']) + "<br>")
               self.events[index].append("<p> <strong> Город: </strong>" + str(self.data[key]['city']) + "<br>")
               self.events[index].append("<strong>Адрес: </strong>" + str(self.data[key]['adress']) + "<br>")
               self.events[index].append("<strong> Дата: " + str(self.data[key]['date']) + "</strong></p>")
                    
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

    def check_outdated(self,json_file):
        with open(json_file, "r",encoding='utf-8') as read_file:
            data_all = json.load(read_file)
        with open("archive_events.json", "r", encoding="utf-8") as file:
            data_old = json.load(file)
        sortkey=datetime.now().year*365+datetime.now().month*30+datetime.now().day
        for key in list(data_all.keys()):
            dt = int(data_all[key]["date"][0:2])+int(data_all[key]["date"][3:5])*30+int(data_all[key]["date"][6:10])*365
            if dt<sortkey:
                with open("archive_events.json", "w", encoding="utf-8") as file:
                    data_old[key] = data_all[key]
                    print(data_old[key])
                    json.dump(data_old, file)
                    data_all.pop(key)
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(data_all, file)
            
    def update_all(self, json_file1,json_file2,json_file3):
        self.events.clear()
        self.render_events.clear()
        self.check_outdated(json_file1)
        self.check_outdated(json_file2)
        self.check_outdated(json_file3)
        with open(json_file1, "r",encoding='utf-8') as read_file1:
            self.data = dict(list(json.load(read_file1).items())+list(self.data.items()))
        with open(json_file2, "r",encoding='utf-8') as read_file2:
            self.data = dict(list(json.load(read_file2).items())+list(self.data.items()))
        with open(json_file3, "r",encoding='utf-8') as read_file3:
            self.data = dict(list(json.load(read_file3).items())+list(self.data.items()))
        sortkey=datetime.now().year*365+datetime.now().month*30+datetime.now().day
        sorted_events = OrderedDict(self.data)
        self.data = dict(OrderedDict(sorted(sorted_events.items(), key=lambda t: int(t[1]["date"][0:2])+int(t[1]["date"][3:5])*30+int(t[1]["date"][6:10])*365-sortkey)))
        #sort 
        index = -1
        for key in list(self.data.keys()):
            dt = int(self.data[key]["date"][0:2])+int(self.data[key]["date"][3:5])*30+int(self.data[key]["date"][6:10])*365
            index+=1
            self.events.append([])

            #for k in self.data[key]:
                    #self.events[index].append(str(self.data[key][k]))
            self.events[index].append("<h2> " + str(self.data[key]['name']) + "<br><strong> " \
                     + str(self.data[key]['status']) + "</strong></h2>")
            self.events[index].append('<p> <li style="list-style-type: none;" > \
                     <a href="#" class="" style="padding: 0px" data-toggle="dropdown" role="button" \
                     aria-haspopup="true" aria-expanded="false"><strong>Инфо</strong> \
                     <span class="caret"></span></a> <ul class="dropdown-menu"> \
                  <li>'+ str(self.data[key]['desc']) +'</li></ul> </li>')
            self.events[index].append('<strong> Страна: </strong>' + str(self.data[key]['country']) + "<br>")
            self.events[index].append("<p> <strong> Город: </strong>" + str(self.data[key]['city']) + "<br>")
            self.events[index].append("<strong>Адрес: </strong>" + str(self.data[key]['adress']) + "<br>")
            self.events[index].append("<strong> Дата: " + str(self.data[key]['date']) + "</strong></p>")
                    
        for i in range(len(self.events)):
            self.render_events.append("".join(self.events[i]))
            self.render_events[i] = '''<div class="col-md-4"> ''' + self.render_events[i] + \
                                        '''<p><a class="btn btn-default" href="/login"> 
                                        Зарегестрироваться &raquo;</a></p> </div>'''



            
