import pygame, sys, PYC

from pygame.constants import MOUSEBUTTONUP
from win32api import GetSystemMetrics
import time, os

SIZE = (int(GetSystemMetrics(0)*0.9),int(GetSystemMetrics(1)*0.9))
pygame.init()
pygame.font.init()



# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CELESTE =(50, 50, 200)
MORADO = (200, 0, 200)
AMARILLO = (255, 255, 0)
FONDO = (0, 0, 10)
GRIS = (20, 20, 20)

# Definir cosas importantes
ventana = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


# Funcion para esperar x segundos

# Clases de un nodo y un grafo

class Nodo():
    # Creacion de un nodo basico
    # Tienes conexiones con otros nodos
    # Y un color tanto exterior como interior(no es diferente de un borde el exterior)
    def __init__(self, pos, name):
        self.connects = []
        self.mark = False
        self.pos = pos
        self.size = SIZE[1]*0.043
        self.width = SIZE[1]*0.05
        self.color_ext = BLANCO
        self.color_in = GRIS
        self.color_label = BLANCO
        self.name = name
        self.dibujarNodo()

    def marcar(self, tiempo = 0):
        self.color_in = BLANCO
        self.color_label = NEGRO
        self.mark = True
   
    def desmarcar(self):
        self.color_label = BLANCO
        self.color_in = GRIS
        self.mark = False
    
    def conectar(self, nodo):
        if nodo not in self.connects:
            self.connects.append(nodo)
    
    def desconectar(self, nodo):
        #desconecta el nodo de otro dado
        if nodo in self.connects:
            self.connects.remove(nodo)

    def dibujarNodo(self):
        # Dibujo del nodo con todos sus componentes
        self.size = SIZE[1]*0.043
        self.draw_in = pygame.draw.circle(ventana, self.color_in, self.pos, self.size)
        self.draw_ext = pygame.draw.circle(ventana, self.color_ext, self.pos, self.size, 5)

        self.font = pygame.font.SysFont('Arial',40)
        self.label = self.font.render(f'{self.name}', True, self.color_label)
        if self.name < 10:
            posTextX = self.pos[0]-8

        else:
            posTextX = self.pos[0]-18

        posTextY = self.pos[1]-25

        ventana.blit(self.label, (posTextX, posTextY))

    def dibujarConexiones(self, color=BLANCO):
        for nodo in self.connects:
            pygame.draw.line(ventana, color , self.pos, nodo.pos, 5)

    def cambiarNombre(self,nombre):
        self.name = nombre
    
    def aislar(self):
        for nodoAd in self.connects:
            nodoAd.connects.remove(self)
        self.connects = []
        
    def focus(self):
        self.color_ext = MORADO

    def unfocus(self):
        self.color_ext = BLANCO

    def isfocus(self):
        if self.color_ext == BLANCO:
            return False
        else:
            return True

class Grafo():
    # Modos:
    # 0 crear Nodo
    # 1 conectar Nodo
    # 2 eliminar Nodo
    # 3 MOVER NODO (al final porque me da miedo hacerla)
    '''
    como el programa de python tenia el buffer activado no podia poner tiempos de espera
    en una misma funcion por lo que cree una cola de animacion donde en cada frame anima
    un nodo distinto
    '''
    def __init__(self):
        self.nodos = []
        self.modos = ["Crear", "Conectar", "Eliminar", "Mover"]
        self.conectando = []
        self.modoE = 0
        self.pila = PYC.Pila()
        self.cola = PYC.Cola()
        self.colaAnimacion = PYC.Cola()
        self.nodoIni = -1
        self.move = False

    def agregarNodo(self, pos):
        nodo = Nodo(pos, len(self.nodos))
        self.nodos.append(nodo)

    def quitarNodo(self,nodo):
        if (nodo in self.nodos):
            for nodoConnect in nodo.connects:
                nodoConnect.connects.remove(nodo)
            self.nodos.remove(nodo)
            i = 0
            for nodo in self.nodos:
                nodo.cambiarNombre(i)
                i +=1 

    def verificarMarcado(self,pos):
        nodo = self.buscarNodoMouse(pos)
        if nodo != -1:
            if self.nodoIni != -1:
                self.nodoIni.desmarcar()
            nodo.marcar()
            self.nodoIni = nodo

    def buscarNodoMouse(self, pos):
        for nodo in self.nodos:
            collideCircle = nodo.draw_in
            if collideCircle.collidepoint(pos):
                return nodo
        return -1

    def cambiarModo(self, select):
        if self.modoE == 1:
            if len(self.conectando) == 1:
                self.conectando[0].unfocus()
            self.conectando = []
        if select:
            self.modoE += 1
        else:
            self.modoE -= 1
        self.modoE = self.modoE % 4

    def conectarNodos(self, nodo1, nodo2):
        if nodo1 in self.nodos and nodo2 in self.nodos:
            nodo1.conectar(nodo2)
            nodo2.conectar(nodo1)

    def accionMouse(self, pos):
        if self.modoE == 0:
            self.agregarNodo(pos)

        elif self.modoE < 5:
            nodo = self.buscarNodoMouse(pos)
            if nodo != -1:
                if self.modoE == 1:
                    if len(self.conectando) == 0:
                        self.conectando.append(nodo)
                        nodo.focus()
                    elif len(self.conectando) == 1 and nodo != self.conectando[0]:
                        self.conectando.append(nodo)
                        self.conectarNodos(self.conectando[0], nodo)
                        self.conectarNodos(nodo, self.conectando[0])
                        self.conectando[0].unfocus()
                        self.conectando = []
                if self.modoE == 2:
                    self.quitarNodo(nodo)
                if self.modoE == 3:
                    nodo.marcar()
                    self.move = nodo

    def animar(self, tiempo):
        if not self.colaAnimacion.vacia():
            variablesAnimation = self.colaAnimacion.obtener()
            nodo = variablesAnimation[0]
            mark = variablesAnimation[1]
            focus = variablesAnimation[2]
            if focus != -1:
                if focus:
                    nodo.focus()
                else:
                    nodo.unfocus()
            if mark != -1:
                if mark:
                    nodo.marcar()
                else:
                    nodo.desmarcar()
            
            time.sleep(tiempo)
            
    def recorridoProfundidad(self, nodo, marks):

        self.focusAnimation(nodo)
        marks.append(nodo)
        self.pila.insertar(nodo)
        self.markAnimation(nodo)
        for nodoAd in nodo.connects:
            if nodoAd not in marks:  
                self.unfocusAnimation(nodo)
                self.recorridoProfundidad(nodoAd, marks)
                self.focusAnimation(nodo)
        
        self.unfocusAnimation(nodo)
        self.pila.eliminar()
       
    def recorridoAncho(self, nodo):
        self.cola.ingresar(nodo)
        while self.cola.cantidad != 0:
            nodoActual = self.cola.actual()
            self.colaAnimacion.ingresar(nodo) # Marcar
            for nodoAd in nodoActual.connects:
                if not self.colaAnimacion.existe(nodoAd):
                    self.colaAnimacion.ingresar(nodoAd) # Marcar
                    self.cola.ingresar(nodoAd)
            self.cola.eliminar()
            
    def limpiar(self):
        self.nodos = []
            
    def eliminarConexiones(self):
        for nodo in self.nodos:
            nodo.aislar()
          
    def quitarMove(self):
        if self.move != self.nodoIni:
            self.move.desmarcar()
        self.move = False

    def desmarcarTodo(self):
        self.nodoIni = -1
        for nodo in self.nodos:
            nodo.desmarcar()
            nodo.unfocus()

    def markAnimation(self, nodo):
        self.colaAnimacion.ingresar((nodo, 1, -1))
    
    def focusAnimation(self, nodo):
        self.colaAnimacion.ingresar((nodo, -1, 1))
        
    def unmarkAnimation(self, nodo):
        self.colaAnimacion.ingresar((nodo, 0, -1))
    
    def unfocusAnimation(self, nodo):
        self.colaAnimacion.ingresar((nodo, -1, 0))
    
    def actualizar(self):
        self.font = pygame.font.SysFont('Arial',40)
        labelModo = self.font.render(
            f'Modo escogido: {self.modos[self.modoE]} Nodo',
             True, 
             BLANCO
            )
        ventana.blit(labelModo, (0,0))

        labelIns = self.font.render(
            "DFS: P ,BFS: O , limpiar:Space",
            True,
            BLANCO
        )
        ventana.blit(labelIns, (0,SIZE[1]-45))
        
        if self.move:
            self.move.pos = pygame.mouse.get_pos()

        for nodo in self.nodos:
            nodo.dibujarConexiones()
        for nodo in self.nodos:
            nodo.dibujarNodo()
        self.animar(0.3)

grafo = Grafo()




while True:
    posMouse = pygame.mouse.get_pos()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit(0)
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                grafo.accionMouse(posMouse)
            if evento.button == 3:
                grafo.verificarMarcado(posMouse)

        if evento.type == MOUSEBUTTONUP:
            print(evento.button)
            if evento.button == 1 and grafo.move:
                grafo.quitarMove()

            if evento.button == 4:
                grafo.cambiarModo(1)

            if evento.button == 5:
                grafo.cambiarModo(0)

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP or evento.key == pygame.K_d:
                grafo.cambiarModo(1)

            if evento.key == pygame.K_DOWN or evento.key == pygame.K_a:
                grafo.cambiarModo(0)
            if evento.key == pygame.K_SPACE:
                grafo.limpiar()
            if evento.key == pygame.K_c:
                grafo.eliminarConexiones()
            if evento.key == pygame.K_x:
                grafo.desmarcarTodo()
                
            if grafo.nodoIni != -1:
                if evento.key == pygame.K_p:
                        grafo.recorridoProfundidad(grafo.nodoIni,[])
                if evento.key == pygame.K_o:
                    grafo.recorridoAncho(grafo.nodoIni)

    ventana.fill(FONDO)
    grafo.actualizar()
    pygame.display.flip()
    clock.tick(120)