class Building:
    def __init__(self, id, name, x, y):
        self.name = name
        self.id = id
        self.x = x
        self.y = y
        self.users = []

    def __str__(self):
        return "%d - %s - (%s, %s)" % (int(self.id), self.name, self.x, self.y)

    def to_dict(self):
        return {'name':self.name,'id':self.id,'x':self.x,'y':self.y}
