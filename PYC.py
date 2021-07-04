class Pila():
    def __init__(self):
        self.contenido = []
        self.cantidad = len(self.contenido)

    def revisarActual(self):
        return self.contenido[self.cantidad-1]
    
    def obtener(self):
        if self.cantidad != 0:
            salida = self.contenido[self.cantidad-1]
            self.contenido.pop()
            self.cantidad = len(self.contenido)
            return salida
    
    def eliminar(self):
        if self.cantidad != 0:
            self.contenido.pop()
            self.cantidad = len(self.contenido)

    def insertar(self, elemento):
        self.contenido.append(elemento)
        self.cantidad = len(self.contenido)
    
    def vaciar(self):
        self.cantidad = 0
        self.contenido = []

class Cola():
    def __init__(self):
        self.contenido = []
        self.cantidad = len(self.contenido)

    def actual(self):
        return self.contenido[0]
    

    def eliminar(self):
        if self.cantidad != 0:
            self.contenido.pop(0)
            self.cantidad = len(self.contenido)

    def obtener(self):
        salida = self.contenido[0]
        self.contenido.pop(0)
        self.cantidad = len(self.contenido)
        return salida
    
    def ingresar(self, elemento):
        self.contenido.append(elemento)
        self.cantidad = len(self.contenido)
    
    def vaciar(self):
        self.cantidad = 0
        self.contenido = []

    def vacia(self):
        if self.cantidad == 0:
            return True
        else:
            return False
        
    def existe(self, elemento):
        if elemento in self.contenido:
            return True
        else:
            return False