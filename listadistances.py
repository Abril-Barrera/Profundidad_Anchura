import json
from distance import Distance

class ListaDistances:
    def __init__(self):
        self.lista = []

    def agregar(self, distance):
        self.lista.append(distance)

    def ordenarDistancia(self, distance):
        return distance.id

    def ordenar_distancia(self):
        self.lista.sort(key=self.ordenarDistancia, reverse=True)