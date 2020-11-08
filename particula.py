class Particula:
    def __init__(self):
        self.id = 0
        self.origenX = 0
        self.origenY = 0
        self.destinoX = 0
        self.destinoY = 0
        self.colorR = 0
        self.colorG = 0
        self.colorB = 0
        self.velocidad = 0

    def __str__(self):
        return "ID: " + str(self.id) + '\n' + \
               "ORIGEN: " + "(" + str(self.origenX) + "," + str(self.origenY) + ")" + '\n' + \
               "DESTINO: " + "(" + str(self.destinoX) + "," + str(self.destinoY) + ")" + '\n' + \
               "COLOR: " + "R: " +str(self.colorR) + ", G:" + str(self.colorG) + ", B: " + str(self.colorB) + '\n' + \
               "VELOCIDAD: " + str(self.velocidad) + '\n'

    def to_dicc(self):
        return{'id': self.id,
               'origen':{'x':self.origenX,'y':self.origenY},
               'destino':{'x':self.destinoX,'y':self.destinoY},
               'velocidad':self.velocidad,
               'color':{'red': self.colorR,'green':self.colorG,'blue':self.colorB}
               }