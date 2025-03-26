from flask import Flask, jsonify, request
from Arbol import Nodo  # Asumiendo que tienes definido Nodo en un archivo separado

app = Flask(__name__)

# Conexiones entre nodos (simulación de tu mapa)
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

# Función DFS iterativa con límite de profundidad
def DFS_prof_iter(nodo, solucion):
    for limite in range(0, 100):
        visitados = []
        sol = buscar_solucion_DFS_Rec(nodo, solucion, visitados, limite)
        if sol is not None:
            return sol
    return None

# Búsqueda recursiva de solución usando DFS
def buscar_solucion_DFS_Rec(nodo, solucion, visitados, limite):
    if limite > 0:
        visitados.append(nodo)
        if nodo.get_datos() == solucion:
            return nodo
        else:
            dato_nodo = nodo.get_datos()
            lista_hijos = []
            for un_hijo in conexiones.get(dato_nodo, []):  
                hijo = Nodo(un_hijo)
                if not hijo.en_lista(visitados):
                    lista_hijos.append(hijo)
            
            nodo.set_hijos(lista_hijos)

            for nodo_hijo in nodo.get_hijos():
                sol = buscar_solucion_DFS_Rec(nodo_hijo, solucion, visitados, limite - 1)
                if sol is not None:
                    return sol
    return None

@app.route('/dfs', methods=['POST'])
def resolver_dfs():
    try:
        data = request.json
        estado_inicial = data.get('estado_inicial', '')
        solucion = data.get('solucion', '')
        
        nodo_inicial = Nodo(estado_inicial)
        nodo = DFS_prof_iter(nodo_inicial, solucion)
        
        if nodo is not None:
            resultado = []
            while nodo is not None:
                resultado.append(nodo.get_datos())
                nodo = nodo.get_padre()
            resultado.reverse()
            return jsonify({'ruta': resultado}), 200
        else:
            return jsonify({'mensaje': 'Solución no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
