import json
import io
import random
from collections import OrderedDict
from datetime import datetime
import os.path
from copy import deepcopy

class RenderEvent:
    def add_url(self, info):
        try:
            info = str(info)
            if "http" in info or "https" in info:
                
                url = info[info.find("https"):len(info)]
            
                return url
        except Exception as e :
            f = open("add_url_debug.txt",'w')
            f.write(str(e))
            f.close()
            return

        
    def __init__(self, json_file):
        self.events = [] 
        self.render_events = []
        self.data = {}
        self.names_list=[]
        if not os.path.exists(json_file):
            with open(json_file, "w",encoding='utf-8') as file:
                    json.dump(self.data,file)
        if not os.path.exists("archive_events.json"):
            with open("archive_events.json", "w",encoding='utf-8') as file:
                    json.dump(self.data,file)
        try:
            self.update(json_file,'*')
        except:
            self.data = {}
            print("feels bad man")

    def update(self, json_file,rank):

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
            self.names_list.clear()
            for key in self.data:
               #print (self.data[key]['desc'])
               self.add_url(self.data[key]['desc'])
               if self.data[key]['status'] == rank or rank == '*':
                   self.names_list.append(key)
                           
                   index+=1
                   self.events.append([])
                   #for k in self.data[key]:
                   self.events[index].append("<h2> " + str(self.data[key]['name']) + "<br><strong> " \
                         + str(self.data[key]['status']) + "</strong></h2>")
                   if "http" in self.data[key]['desc'] or "https" in self.data[key]['desc']:
                       new_data = str(self.data[key]['desc'])
                       new_data = new_data[0:new_data.find("https")]
                       print(new_data)
                       self.events[index].append('<p> <li style="list-style-type: none;" > \
                             <a href="#" class="" style="padding: 0px" data-toggle="dropdown" role="button" \
                             aria-haspopup="true" aria-expanded="false"><strong>Инфо</strong> \
                             <span class="caret"></span></a> <ul class="dropdown-menu"> \
                          <li>'+ str(new_data) + '<a href = "' +self.add_url(self.data[key]['desc'])+'" >'  +'Ссылка </a></li></ul> </li>')
                   else:
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
                                        '''<p><a class="btn btn-default" href="/login/'''+self.names_list[i]+'''"> 
                                        Зарегестрироваться &raquo;</a></p> </div>'''

    def admin_update(self, json_file,rank):
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
            self.names_list.clear()
            for key in self.data:
               if self.data[key]['status'] == rank or rank == '*':
                   self.names_list.append(key)
                   #print (self.data[key]['date'])        
                   index+=1
                   self.events.append([])
                   print(self.data[key][desc])
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
                self.render_events[i] = '''<form method="post">
                                        <div class="col-md-4"> ''' + self.render_events[i] + \
                                        '''<p><input type="submit" class = "btn btn-primary mb-2" value="Удалить"
                                        name="r'''+self.names_list[i]+'''"></p> 
                                        <p><input type="submit" class = "btn btn-primary mb-2" value="Изменить"
                                        name="'''+self.names_list[i]+'''"></p> </form> </div>'''

    def save_new_event(self, new_event, event_name, json_file):
        with open(json_file, "r",encoding='utf-8') as read_file:
            self.data = json.load(read_file)
        with open(json_file, "w", encoding="utf-8") as file:
            self.data[event_name + str(random.randint(0,4214231312))] = new_event
            json.dump(self.data, file)

    def update_event(self, event, event_name, json_file):
        with open(json_file, "r",encoding='utf-8') as read_file:
            self.data = json.load(read_file)
        with open(json_file, "w", encoding="utf-8") as file:
            self.data[event_name] = event
            json.dump(self.data, file)

    def destroy_event(self, event_name, json_file):
        with open(json_file, "r",encoding='utf-8') as read_file:
            self.data = json.load(read_file)
            self.data.pop(event_name)
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file)

    def get_existing_event(self,key,json_file):
        with open(json_file, "r",encoding='utf-8') as read_file:
            self.data = json.load(read_file)
            return self.data[key]

    def get_event_names(self,rank,json_file):
        with open(json_file, "r",encoding='utf-8') as read_file:
            self.data = json.load(read_file)
        self.names_list.clear()
        for key in self.data:
            if self.data[key]['status'] == rank or rank == '*':
                self.names_list.append(key)
        return self.names_list

    def get_pure_events(self,rank, json_file):
        data={}
        with open(json_file, "r",encoding='utf-8') as read_file:
            self.data = json.load(read_file)
        for key in self.data:
            if self.data[key]['status'] == rank or rank == '*':
                data[key]=self.data[key]
        return data

    def get_render_events(self):
        events=deepcopy(self.render_events)
        return events

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
                    #print(data_old[key])
                    json.dump(data_old, file)
                    data_all.pop(key)
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(data_all, file)



            
