class Event:
    def __init__(self):
        self.name = None
        self.status = None
        self.city = None
        self.desc = None
        self.country = None
        self.adress = None
        self.date = None
        self.event = {}
    def make_event(self):
        self.event = {"name":str(self.name),
                     "country":self.country,
                     "status":self.status,
                     "desc":self.desc,
                     "city":self.city,
                     "adress":self.adress,
                     "date":self.date.strftime("%d-%m-%Y")}
        print(self.event)
        return self.event

    def mark_event(self):
        self.event = {"name":"<h2> " + str(self.name) + "<br><strong> " \
                     + self.status + "</strong></h2>",
                     "desc":'<p> <li style="list-style-type: none;" > \
                     <a href="#" class="" style="padding: 0px" data-toggle="dropdown" role="button" \
                     aria-haspopup="true" aria-expanded="false"><strong>Инфо</strong> \
                     <span class="caret"></span></a> <ul class="dropdown-menu"> \
                  <li>'+ self.desc +'</li></ul> </li>', \
                     "country":'<strong> Страна: </strong>' + self.country + "<br>",
                     "city":"<p> <strong> Город: </strong>" + self.city + "<br>",
                     " adress": "<strong>Адрес: </strong>" + self.adress + "<br>",
                     "date":"<strong> Дата: " + self.date.strftime("%d-%m-%Y") + "</strong></p>"}
        print(self.event)
        return self.event

              