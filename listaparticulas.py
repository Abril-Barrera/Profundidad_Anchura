import json
from particula import Particula

class ListaParticulas:
    def __init__(self):
        self.lista = []

    def ordenarVelocidad(self, particula):
        return particula.velocidad

    def ordenar_velocidad(self):
        self.lista.sort(key=self.ordenarVelocidad, reverse= True) #self.lista.sort(key=self.ordenarDistancia, reverse = true)

    def ordenarDistancia(self,):
        return distance

    def ordenar_distancia(self):
        print('x')#self.lista.sort(key=self.ordenarDistancia, reverse=True)

    def agregar(self, particula):
        self.lista.append(particula)

    def mostrar(self):
        for particula in self.lista:
            print(particula)

    def guardar(self, file):

        lista_dicc = []
        for particula in self.lista:
            lista_dicc.append(particula.to_dicc())

        with open(file, 'w') as archivo:
            json.dump(lista_dicc,archivo, indent=5)

    def recuperar(self,file):
        with open(file,'r') as archivo:
            listaparticulas = json.load(archivo)

            for particula in listaparticulas:
                p = Particula()
                p.id = particula['id']
                p.origenX = particula['origen']['x']
                p.origenY = particula ['origen']['y']
                p.destinoX = particula['destino']['x']
                p.destinoY = particula['destino']['y']
                p.velocidad = particula['velocidad']
                p.colorR = particula['color']['red']
                p.colorG = particula['color']['green']
                p.colorB = particula['color']['blue']
                self.lista.append(p)




