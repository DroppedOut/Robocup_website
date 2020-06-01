import sqlite3
class Team:
    def __init__(self, name, mem1, mem2, mem3, mem4, mentor, league, event):
        self.name = name
        self.mem1 = mem1
        self.mem2 = mem2
        self.mem3 = mem3
        self.mem4 = mem4
        self.mentor = mentor
        self.league = league
        self.event = event
        self.text = "no text yet"
        f = open('send.txt', 'w+')
        f.seek(0)
        f.close()
    def insert(self):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()

        query = "INSERT INTO teams VALUES(?,?,?,?,?,?,?,?)"
        cur.execute(query, (self.name, self.mem1, self.mem2 ,
                            self.mem3, self.mem4, self.mentor, self.league, self.event))

        conn.commit()
        conn.close()
    def get_text(self):
        self.text = \
        'Event name:' + self.event + '\n' + \
        'Team name:' + self.name + '\n' + \
        'Member 1 name:' + self.mem1 + '\n' + \
        'Member 2 name:' + self.mem2 + '\n' + \
        'Member 3 name:' + self.mem3 + '\n' + \
        'Member 4 name:' + self.mem4 + '\n' + \
        'Mentor name:'   + self.mentor + '\n' + \
        'League:' + self.league + '\n'
        return self.text
    def write(self):
        f = open('send.txt', 'w')
        f.write(self.text)
        f.close()