from flask import Flask, request, render_template
from Arbol import Nodo

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

# Función DFS iterativa
def DFS_prof_iter(nodo, solucion):
    for limite in range(0, 100):
        visitados = []
        sol = buscar_solucion_DFS_Rec(nodo, solucion, visitados, limite)
        if sol is not None:
            return sol
    return None

# Función recursiva para la búsqueda DFS
def buscar_solucion_DFS_Rec(nodo, solucion, visitados, limite):
    if limite > 0:
        visitados.append(nodo)

        # Si encontramos la solución, retornamos el nodo
        if nodo.get_datos() == solucion:
            return nodo
        
        # Expandir nodos hijos
        lista_hijos = []
        for un_hijo in conexiones.get(nodo.get_datos(), []):
            hijo = Nodo(un_hijo)
            if not hijo.en_lista(visitados):
                hijo.set_padre(nodo)
                lista_hijos.append(hijo)

        nodo.set_hijos(lista_hijos)

        # Recursión para cada hijo
        for nodo_hijo in nodo.get_hijos():
            sol = DFS_prof_iter(nodo_hijo, solucion)
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
    nodo = DFS_prof_iter(nodo_inicial, solucion)

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
