class Log:
    def __init__(self, id, user_id, x, y, building = 'No building', message =''):

        self.user_id = user_id
        self.id = id
        self.x = x
        self.y = y
        self.building = building
        self.nearby = 10 #pensar no default que queremos
        self.message = message

    def __str__(self):
        return "%d - %s - (%s, %s)" % (int(self.id), self.user_id, self.x, self.y)

    def to_dict(self):
        return {'id':self.id,'userId':self.user_id,'x':self.x,'y':self.y,'building':self.building}
