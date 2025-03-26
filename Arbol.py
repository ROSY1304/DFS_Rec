class Nodo:
    def __init__(self, datos):
        self.datos = datos
        self.padre = None
        self.hijos = []

    def get_datos(self):
        return self.datos

    def get_padre(self):
        return self.padre

    def set_padre(self, padre):
        self.padre = padre

    def set_hijos(self, hijos):
        self.hijos = hijos

    def get_hijos(self):
        return self.hijos

    def en_lista(self, lista):
        # Este método verifica si el nodo está en la lista de visitados
        return self in lista
