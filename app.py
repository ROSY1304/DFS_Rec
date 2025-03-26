from flask import Flask, request, render_template
from Arbol import Nodo
from DFS_prof import DFS_prof_iter
app = Flask(__name__)

# Definir conexiones de ciudades
conexiones = {
    'EDO.MEX': {'QRO', 'SLP', 'SONORA'},
    'PUEBLA': {'HIDALGO', 'SLP'},
    'CDMX': {'MICHOACAN'},
    'MICHOACAN': {'SONORA'},
    'SLP': {'QRO', 'PUEBLA', 'EDO.MEX', 'SONORA', 'GUADALAJARA'},
    'QRO': {'EDO.MEX', 'SLP'},
    'HIDALGO': {'PUEBLA', 'GUADALAJARA', 'SONORA'},
    'MONTERREY': {'HIDALGO', 'SLP'},
    'SONORA': {'MONTERREY', 'HIDALGO', 'SLP', 'EDO.MEX', 'MICHOACAN'}
}

def DFS_Rec(nodo, solucion, visitados, limite):
    """ Búsqueda en profundidad recursiva con límite. """
    if limite > 0:
        visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo
        
        # Expandir nodos hijos
        lista_hijos = []
        for un_hijo in conexiones.get(nodo.get_datos(), []):
            hijo = Nodo(un_hijo)
            if not hijo.en_lista(visitados):
                hijo.set_padre(nodo)  # Asignar el nodo padre
                lista_hijos.append(hijo)

        nodo.set_hijos(lista_hijos)

        for nodo_hijo in nodo.get_hijos():
            sol = DFS_Rec(nodo_hijo, solucion, visitados, limite - 1)
            if sol is not None:
                return sol

    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    # Obtener el estado inicial y el estado final desde el formulario
    estado_inicial = request.form['estado_inicial']
    solucion = request.form['solucion']
    visitados = []
    
    # Inicializar el nodo inicial
    nodo_inicial = Nodo(estado_inicial)
    nodo = None
    
    # Realizar la búsqueda DFS con límite de profundidad
    for limite in range(0, 100):  # Iteración sobre profundidad limitada
        nodo = DFS_Rec(nodo_inicial, solucion, visitados, limite)
        if nodo is not None:
            break

    # Preparar el resultado
    resultado = []
    if nodo:
        while nodo is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
    else:
        resultado = ["No se encontró una solución"]

    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
