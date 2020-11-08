from PySide2.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QGraphicsScene
from UI_mainWindow import Ui_MainWindow
from PySide2.QtCore import Slot
from particula import Particula
from listaparticulas import ListaParticulas
from distance import Distance
from listadistances import ListaDistances
import math
from PySide2.QtGui import QPen, QColor, QBrush
import pprint
import os
aux = 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.listaparticulas = ListaParticulas()
        self.listadistances = ListaDistances()

        self.ui.pbGuardar.clicked.connect(self.click)
        self.ui.pbMostrar.clicked.connect(self.mostrar)
        self.ui.pbLimpiar.clicked.connect(self.clear)
        self.ui.actionGuardar.triggered.connect(self.guardarArchivo)
        self.ui.actionAbrir.triggered.connect(self.abrir)
        self.ui.pbVisualizar.clicked.connect(self.visualizar)
        self.ui.pbOrdenarDistancia.clicked.connect(self.ordenar_distancia)
        self.ui.pbOrdenarVelocidad.clicked.connect(self.ordenar_velocidad)
        self.ui.aVerPuntos.triggered.connect(self.ver_puntos)
        self.ui.aPuntosCercanos.triggered.connect(self.puntos_cercanos)
        self.ui.pbMostrarGrafo.clicked.connect(self.mostrarGrafo)
        self.ui.aRecorridoProfundidad.triggered.connect(self.recorridoProfundidad)
        self.ui.aRecorridoAnchura.triggered.connect(self.recorridoAnchura)
        self.ui.aPrim.triggered.connect(self.prim)
        self.ui.aKruskal.triggered.connect(self.kruskal)
        self.ui.aMostrar.triggered.connect(self.mostrarGrafoOriginal)

    @Slot()
    def mostrar(self):
        distance = Distance()
        #self.listaparticulas.mostrar()
        for particula in self.listaparticulas.lista:
            self.ui.plainTextEdit.insertPlainText(str(particula))
            v1 = float(int(particula.destinoX) - int(particula.origenX))
            v2 = float(int(particula.destinoY) - int(particula.origenY))
            distancia = float(math.sqrt((v1) ** 2 + (v2) ** 2))
            self.ui.plainTextEdit.insertPlainText(" -> Distancia: " + str(distancia) + '\n\n')


            distance.id = distancia
            distance.colorR = particula.colorR
            distance.colorG = particula.colorG
            distance.colorB = particula.colorB
            self.listadistances.agregar(distance)


    @Slot()
    def visualizar(self):
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 500, 500)
        self.ui.graphicsView.setScene(self.scene)

        self.pen = QPen()
        self.pen.setColor(QColor(0, 0, 0))
        self.pen.setWidth(3)

        self.scene.addLine(0, 0, 499, 0, self.pen)
        self.scene.addLine(0, 499, 499, 499, self.pen)
        self.scene.addLine(0, 0, 0, 499, self.pen)
        self.scene.addLine(499, 0, 499, 499, self.pen)
        
        for particula in self.listaparticulas.lista:
            self.pen.setColor(QColor(particula.colorR, particula.colorG, particula.colorB))
            self.scene.addLine(particula.origenX, particula.origenY, particula.destinoX, particula.destinoY, self.pen)

            self.scene.addEllipse(particula.origenX, particula.origenY, 5, 5, self.pen, QBrush(QColor(50, 100, 0)))
            self.scene.addEllipse(particula.destinoX, particula.destinoY, 5, 5, self.pen, QBrush(QColor(100, 0, 0)))
    @Slot()
    def click(self):
        id = self.ui.leID.text()
        origenX = self.ui.leORIGENx.text()
        origenY = self.ui.leORIGENy.text()
        destinoX = self.ui.leDESTINOx.text()
        destinoY = self.ui.leDESTINOy.text()
        colorR = self.ui.leCOLORr.text()
        colorG = self.ui.leCOLORg.text()
        colorB = self.ui.leCOLORb.text()
        velocidad = self.ui.leVELOCIDAD.text()
        v1= float(int(destinoX)-int(origenX))
        v2 = float(int(destinoY)-int(origenY))
        distancia = float(math.sqrt((v1)**2 + (v2)**2))
        print(id,origenX,origenY,destinoX,destinoY,colorR,colorG,colorB,velocidad, distancia)

        particula = Particula()
        particula.id = int(id)
        particula.origenX = int(origenX)
        particula.origenY = int(origenY)
        particula.destinoX = int(destinoX)
        particula.destinoY = int(destinoY)
        particula.colorR = int(colorR)
        particula.colorG = int(colorG)
        particula.colorB = int(colorB)
        particula.velocidad = int(velocidad)
        self.ui.lcdDistancia.display(distancia)

        self.listaparticulas.agregar(particula)

        msg = QMessageBox.information(self,'Éxito', 'Se agregó paquete con éxito')
        #clear()

    @Slot()
    def clear(self):
        self.ui.leID.clear()
        self.ui.leORIGENx.clear()
        self.ui.leORIGENy.clear()
        self.ui.leDESTINOx.clear()
        self.ui.leDESTINOy.clear()
        self.ui.leCOLORr.clear()
        self.ui.leCOLORg.clear()
        self.ui.leCOLORb.clear()
        self.ui.leVELOCIDAD.clear()
    @Slot()
    def abrir(self):
        print('abrir')
        file = QFileDialog.getOpenFileName(self, 'Abrir archivo', '.', 'JSON (*.json)')
        self.listaparticulas.recuperar(file[0])

    @Slot()
    def ordenar_distancia(self):
        print('click')
        self.listaparticulas.ordenar_distancia()

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 400, 1000)
        self.ui.graphicsView.setScene(self.scene)

        self.pen = QPen()
        self.pen.setColor(QColor(0,0,0))
        self.pen.setWidth(3)

        i = 1
        for particula in self.listaparticulas.lista:
            self.pen.setColor(QColor(particula.colorR, particula.colorG, particula.colorB))
            v1 = float(int(particula.destinoX) - int(particula.origenX))
            v2 = float(int(particula.destinoY) - int(particula.origenY))
            distancia = float(math.sqrt((v1) ** 2 + (v2) ** 2))
            self.scene.addLine(0, i, distancia, i, self.pen)
            i = i+1


    @Slot()
    def ordenar_velocidad(self):
        print('click')
        self.listaparticulas.ordenar_velocidad()

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 400, 1000)
        self.ui.graphicsView.setScene(self.scene)

        self.pen = QPen()
        self.pen.setColor(QColor(0,0,0))
        self.pen.setWidth(3)

        i = 1
        for particula in self.listaparticulas.lista:
            self.pen.setColor(QColor(particula.colorR, particula.colorG, particula.colorB))
            self.scene.addLine(0, i, particula.velocidad, i, self.pen)
            i = i+1

    @Slot()
    def guardarArchivo(self):
        file = QFileDialog.getSaveFileName(self, 'Guardar archivo...', '.', 'JSON(*.json)')
        print(file)
        self.listaparticulas.guardar(file[0])

    @Slot()
    def ver_puntos(self):

        self.scene = QGraphicsScene()
        #self.scene.setSceneRect(0, 0, 400, 1000)
        self.ui.graphicsView.setScene(self.scene)

        self.pen = QPen()
        self.pen.setColor(QColor(0, 0, 0))
        self.pen.setWidth(3)

        listaPuntos = list()

        for particula in self.listaparticulas.lista:
            self.pen.setColor(QColor(particula.colorR, particula.colorG, particula.colorB))
            self.scene.addEllipse(particula.origenX, particula.origenY, 3, 3, self.pen, QBrush(QColor(particula.colorR,particula.colorG, particula.colorB)))
            self.scene.addEllipse(particula.destinoX, particula.destinoY, 3, 3, self.pen, QBrush(QColor(particula.colorR, particula.colorG, particula.colorB)))
            origen = (particula.origenX,particula.origenY)
            destino = (particula.destinoX, particula.destinoY)
            listaPuntos.append(origen)
            listaPuntos.append(destino)

        #print(listaPuntos)

    @Slot()
    def puntos_cercanos(self):

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        self.pen = QPen()
        self.pen.setWidth(1)

        listaPuntos = list()
        listaColores = list()

        for particula in self.listaparticulas.lista:
            self.pen.setColor(QColor(particula.colorR, particula.colorG, particula.colorB))
            self.scene.addEllipse(particula.origenX, particula.origenY, 3, 3, self.pen, QBrush(QColor(particula.colorR, particula.colorG, particula.colorB)))
            self.scene.addEllipse(particula.destinoX, particula.destinoY, 3, 3, self.pen, QBrush(QColor(particula.colorR, particula.colorG, particula.colorB)))
            origen = (particula.origenX, particula.origenY)
            destino = (particula.destinoX, particula.destinoY)
            origenColores = (particula.colorR,particula.colorG, particula.colorB)
            destinoColores = (particula.colorR, particula.colorG, particula.colorB)
            listaPuntos.append(origen)
            listaPuntos.append(destino)
            listaColores.append(origenColores)
            listaColores.append(destinoColores)

        #print(listaColores)
        #print(listaPuntos)
        for i in range(0, len(listaPuntos)):
            auxI = listaPuntos[i]
            distancia = 1000000000000000

            for y in range(0, len(listaPuntos)):
                auxY = listaPuntos[y]

                if (auxI[0] != auxY[0] or auxI[1] != auxY[1]):
                    v1 = float(int(auxY[0]) - int(auxI[0]))
                    v2 = float(int(auxY[1]) - int(auxI[1]))
                    distanciaActual = float(math.sqrt((v1) ** 2 + (v2) ** 2))

                    #print('distancia: ', distanciaActual)

                    if (distanciaActual <= distancia):
                        distancia = distanciaActual
                        colores = listaColores[i-1]
                        auxR = colores[0]
                        auxG = colores[1]
                        auxB = colores[2]
                        x = auxY[0]
                        z = auxY[1]

                if (y == (len(listaPuntos)-1)):

                    self.pen.setColor(QColor(auxR, auxG, auxB))
                    #print('ACTUAL: ',auxI[0],auxI[1])
                    #print('MÁS CERCANO ', x, z)
                    self.pen.setWidth(1)
                    self.scene.addLine(auxI[0], auxI[1], x, z , self.pen)

    @Slot()
    def mostrarGrafo(self):
        grafo = dict()

        for particula in self.listaparticulas.lista:
            pOrigen = str(particula.origenX) + ('.') + str(particula.origenY)
            pDestino = str(particula.destinoX) + ('.') + str(particula.destinoY)

            v1 = float(int(particula.destinoX) - int(particula.origenX))
            v2 = float(int(particula.destinoY) - int(particula.origenY))
            distancia = float(math.sqrt((v1) ** 2 + (v2) ** 2))

            origen = pOrigen
            destino = pDestino
            peso = int(distancia)

            if origen in grafo:
                grafo[origen].append((destino, peso))
            else:
                grafo[origen] = [(destino, peso)]
            if destino in grafo:
                grafo[destino].append((origen, peso))
            else:
                grafo[destino] = [(origen, peso)]

        cadena = pprint.pformat(grafo, width=40)
        self.ui.plainTextEdit.insertPlainText(str(cadena))

    @Slot()
    def recorridoProfundidad(self):
        grafo = dict()

        for particula in self.listaparticulas.lista:
            pOrigen = str(particula.origenX) + ('.') + str(particula.origenY)
            pDestino = str(particula.destinoX) + ('.') + str(particula.destinoY)

            origen = pOrigen
            destino = pDestino

            if origen in grafo:
                grafo[origen].append(destino)
            else:
                grafo[origen] = [destino]
            if destino in grafo:
                grafo[destino].append(origen)
            else:
                grafo[destino] = [origen]

        visitados = []
        pila = []
        eleccion = self.ui.origenGrafo.text()
        pila.append(eleccion)

        if eleccion in grafo.keys():
            while pila:
                eleccion = pila.pop()
                if eleccion not in visitados:
                    visitados.append(eleccion)
                for vecino in grafo[eleccion]:
                    if vecino not in visitados:
                        pila.append(vecino)
            self.ui.plainTextEdit.insertPlainText(str(visitados))

    @Slot()
    def recorridoAnchura(self):
        grafo = dict()

        for particula in self.listaparticulas.lista:
            pOrigen = str(particula.origenX) + ('.') + str(particula.origenY)
            pDestino = str(particula.destinoX) + ('.') + str(particula.destinoY)

            origen = pOrigen
            destino = pDestino

            if origen in grafo:
                grafo[origen].append(destino)
            else:
                grafo[origen] = [destino]
            if destino in grafo:
                grafo[destino].append(origen)
            else:
                grafo[destino] = [origen]

        cadena = pprint.pformat(grafo, width=40)
        print(cadena)
        # self.ui.plainTextEdit.insertPlainText(str(cadena))

        visitados = []
        cola = []
        eleccion = self.ui.origenGrafo.text()
        #eleccion = "72.321"
        cola.insert(0, eleccion)
        visitados.append(eleccion)

        if eleccion in grafo.keys():
            while cola:
                eleccion = cola.pop()
                if eleccion not in visitados:
                    visitados.append(eleccion)
                for vecino in grafo[eleccion]:
                    if vecino not in visitados:
                        cola.insert(0, vecino)

            print("=========Resultados=========")
            print("Visitados:", visitados)
            print("Cola:", cola)
            self.ui.plainTextEdit.insertPlainText(str(visitados))
            # os.system("pause")
        else:
            print("No existe")


    @Slot()
    def prim(self):
        grafo = dict()

        for particula in self.listaparticulas.lista:
            pOrigen = str(particula.origenX) + ('.') + str(particula.origenY)
            pDestino = str(particula.destinoX) + ('.') + str(particula.destinoY)

            v1 = float(int(particula.destinoX) - int(particula.origenX))
            v2 = float(int(particula.destinoY) - int(particula.origenY))
            distancia = float(math.sqrt((v1) ** 2 + (v2) ** 2))

            origen = pOrigen
            destino = pDestino
            peso = int(distancia)

            if origen in grafo:
                grafo[origen].append((destino, peso))
            else:
                grafo[origen] = [(destino, peso)]
            if destino in grafo:
                grafo[destino].append((origen, peso))
            else:
                grafo[destino] = [(origen, peso)]

        cadena = pprint.pformat(grafo, width=40)
        #print(cadena)

        visitados = []
        grafoResultante = dict()
        colaPrioridad = []
        eleccion = self.ui.origenGrafo.text()
        #eleccion = "400.200"
        visitados.append(eleccion)
        for vecino in grafo[eleccion]:
            adya = (eleccion,) + vecino
            if adya not in colaPrioridad:
                colaPrioridad.insert(0, adya)

        while len(colaPrioridad) != 0:
            aux = 10000000000000
            for adyacente in colaPrioridad:
                if adyacente[1] not in visitados:
                    if adyacente[0] == visitados[-1]:
                        pesoD = adyacente[2]
                        if pesoD < aux:
                            aux = pesoD
                            eliminado = adyacente

            if len(colaPrioridad) != 0:
                if eliminado in colaPrioridad:
                    colaPrioridad.remove(eliminado)
                else:
                    colaPrioridad.clear()

            if eliminado[1] not in visitados:
                visitados.append(eliminado[1])

                for adyacente in grafo[eliminado[1]]:
                    adya = (eliminado[1],) + adyacente
                    if adya not in colaPrioridad:
                        colaPrioridad.insert(0, adya)
                grafoResultante[eliminado[0]] = [(eliminado[1], eliminado[2])]

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 600)
        self.ui.graphicsView.setScene(self.scene)

        self.pen = QPen()

        longitud = len(grafoResultante)
        contador = 0

        for item in grafoResultante.items():
            #print(item)
            puntoO = item[0]
            puntoD = item[1][0][0]
            #print('Punto O', puntoO)
            #print('Punto D',puntoD)
            origenX = int(puntoO.split(".", 2)[0])
            origenY = int(puntoO.split(".", 2)[1])
            destinoX = int(puntoD.split(".", 2)[0])
            destinoY = int(puntoD.split(".", 2)[0])
            self.scene.addEllipse(origenX, origenY, 5, 5, self.pen, QBrush(QColor(50, 100, 0)))
            contador = contador +1
            if contador == longitud:
                self.scene.addEllipse(int(item[1][0][0].split(".", 2)[0]), int(item[1][0][0].split(".", 2)[1]), 5, 5, self.pen, QBrush(QColor(50, 100, 0)))
            self.scene.addLine(int(item[0].split(".", 2)[0]), int(item[0].split(".", 2)[1]),int(item[1][0][0].split(".", 2)[0]), int(item[1][0][0].split(".", 2)[1]))

    @Slot()
    def mostrarGrafoOriginal(self):

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 500, 500)
        self.ui.graphicsView.setScene(self.scene)

        self.pen = QPen()
        self.pen.setColor(QColor(0, 100, 0))
        self.pen.setWidth(3)

        #self.scene.addLine(0, 0, 499, 0, self.pen)
        #self.scene.addLine(0, 499, 499, 499, self.pen)
        #self.scene.addLine(0, 0, 0, 499, self.pen)
        #self.scene.addLine(499, 0, 499, 499, self.pen)

        for particula in self.listaparticulas.lista:
            #self.pen.setColor(QColor(particula.colorR, particula.colorG, particula.colorB))
            self.scene.addLine(particula.origenX, particula.origenY, particula.destinoX, particula.destinoY, self.pen)

            self.scene.addEllipse(particula.origenX, particula.origenY, 5, 5, self.pen, QBrush(QColor(50, 100, 0)))
            self.scene.addEllipse(particula.destinoX, particula.destinoY, 5, 5, self.pen, QBrush(QColor(100, 0, 0)))

    @Slot()
    def kruskal(self):

        def MAKE_SET(x):
            return [x]

        def FIND_SET(x, list):
            i = 0
            for element in list:
                try:
                    index= element.index(x)
                    return i
                except:
                    pass
                    #print("This is an error message!")
                i = i + 1
        def UNION(index_u, index_v,lista):
            L = lista[index_u]
            T = lista[index_v]

            lista.remove(L)
            lista.remove(T)

            final_list = list(set(L + T))
            lista.append(final_list)

            return lista

        grafoResultante = []
        colaPrioridad = []
        disjointSet = []

        for particula in self.listaparticulas.lista:
            pOrigen = str(particula.origenX) + ('.') + str(particula.origenY)
            pDestino = str(particula.destinoX) + ('.') + str(particula.destinoY)

            v1 = float(int(particula.destinoX) - int(particula.origenX))
            v2 = float(int(particula.destinoY) - int(particula.origenY))
            distancia = float(math.sqrt((v1) ** 2 + (v2) ** 2))

            origen = pOrigen
            destino = pDestino
            peso = int(distancia)

            arista = [origen,destino,peso]
            colaPrioridad.append(arista)

            disjointSet.append(MAKE_SET(origen))
            disjointSet.append(MAKE_SET(destino))


        colaPrioridad.sort(key=lambda x: x[2])
        disjointSet = [ii for n, ii in enumerate(disjointSet) if ii not in disjointSet[:n]]

        i = 0
        print(disjointSet)
        if len(colaPrioridad) != 0:

            for element in colaPrioridad:
                index_u = FIND_SET(element[0], disjointSet)
                index_v = FIND_SET(element[1], disjointSet)


                if FIND_SET(element[0],disjointSet) != FIND_SET(element[1],disjointSet):
                    grafoResultante.append(element)
                    disjointSet = UNION(index_u,index_v, disjointSet)
                i = i + 1

            print(disjointSet)

        print('  -> AEM ', grafoResultante)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 600)
        self.ui.graphicsView.setScene(self.scene)

        self.pen = QPen()

        for item in grafoResultante:
            puntoO = item[0]
            puntoD = item[1]

            origenX = int(puntoO.split(".", 2)[0])
            origenY = int(puntoO.split(".", 2)[1])
            destinoX = int(puntoD.split(".", 2)[0])
            destinoY = int(puntoD.split(".", 2)[1])

            self.scene.addEllipse(origenX, origenY, 5, 5, self.pen, QBrush(QColor(100, 100, 0)))
            self.scene.addEllipse(destinoX, destinoY, 5, 5, self.pen, QBrush(QColor(100, 100, 0)))
            self.scene.addLine(int(item[0].split(".", 2)[0]), int(item[0].split(".", 2)[1]), int(item[1].split(".", 2)[0]), int(item[1].split(".", 2)[1]))
