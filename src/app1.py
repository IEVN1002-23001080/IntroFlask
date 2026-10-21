import os
import math
from flask import Flask, render_template, request

# Rutas absolutas a bas_flask/templates y bas_flask/static
basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(os.path.dirname(basedir), 'bas_flask', 'templates')
static_dir = os.path.join(os.path.dirname(basedir), 'bas_flask', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# --- Ruta Principal / Index ---
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# --- Ruta Operaciones Básicas ---
@app.route('/operasbas', methods=['GET', 'POST'])
def operasbas():
    res = None
    n1 = 0
    n2 = 0

    if request.method == 'POST':
        n1 = request.form.get('n1')
        n2 = request.form.get('n2')

        if (operacion := request.form.get('operacion')) == 'sumar':
            res = float(n1) + float(n2)
        elif operacion == 'restar':
            res = float(n1) - float(n2)
        elif operacion == 'multiplicar':
            res = float(n1) * float(n2)

    return render_template("operasbas.html", res=res, n1=n1, n2=n2)

# --- Ruta Distancia entre 2 Puntos ---
@app.route('/distancia', methods=['GET', 'POST'])
def distancia():
    res = None
    x1 = ""
    y1 = ""
    x2 = ""
    y2 = ""

    if request.method == 'POST':
        x1 = request.form.get('x1')
        y1 = request.form.get('y1')
        x2 = request.form.get('x2')
        y2 = request.form.get('y2')

        res = math.sqrt((float(x2) - float(x1))**2 + (float(y2) - float(y1))**2)

    return render_template("distancia.html", res=res, x1=x1, y1=y1, x2=x2, y2=y2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)