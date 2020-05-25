import json
import io
class Test:
    def __init__(self):
        self.events = [] 
        self.render_events = []    
        with open("events.json", "r",encoding = 'utf-8') as read_file:
            self.data = json.load(read_file)
            print(read_file)
            #print (self.data)
            index = -1
            for key in self.data:
               print(index)                
               index+=1
               self.events.append([])
               for k in self.data[key]:
                    self.events[index].append(str(self.data[key][k]))
            for i in range(len(self.events)):
                self.render_events.append("".join(self.events[i]))
                self.render_events[i] = '''<div class="col-md-4"> ''' + self.render_events[i] + \
                                        '''<p><a class="btn btn-default" href="/login"> 
                                        Зарегестрироваться &raquo;</a></p> </div>'''
                self.render_events = self.render_events[i].splitlines()
                print(self.render_events)
 
        def render_events(self):
              return self.render_events
            
