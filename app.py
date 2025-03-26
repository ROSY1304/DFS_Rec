from flask import Flask, request, render_template
from Arbol import Nodo
from DFS_prof import buscar_solucion_DFS_Rec

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    estado_inicial = list(map(int, request.form['estado_inicial'].split(',')))
    solucion = list(map(int, request.form['solucion'].split(',')))
    visitados = []
    nodo_inicial = Nodo(estado_inicial)
    nodo = buscar_solucion_DFS_Rec(nodo_inicial, solucion, visitados)

    resultado = []
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()

    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
