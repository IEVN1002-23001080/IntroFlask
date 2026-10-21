import os
from flask import Flask, render_template, request

basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(os.path.dirname(basedir), 'bas_flask', 'templates')
static_dir = os.path.join(os.path.dirname(basedir), 'bas_flask', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

ventas = []

@app.route('/', methods=['GET', 'POST'])
def cinepolis():
    valorPagar = None
    mensaje = ''
    nombre = ''
    compradores = ''
    tarjeta = 'No'
    boletos = ''

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        compradores = request.form.get('cantidadCompradores', '')
        tarjeta = request.form.get('tarjetaCineco', 'No')
        boletos = request.form.get('cantidadBoletos', '')

        try:
            compradores = int(compradores)
            boletos = int(boletos)

            if nombre == '':
                mensaje = 'Escribe el nombre del comprador.'
            elif compradores <= 0 or boletos <= 0:
                mensaje = 'Las cantidades deben ser mayores que cero.'
            elif boletos > compradores * 7:
                mensaje = 'La cantidad de boletos supera el máximo permitido.'
            elif tarjeta not in ['Si', 'No']:
                mensaje = 'Selecciona si tienes tarjeta Cineco.'
            else:
                total = boletos * 12

                if boletos > 5:
                    total = total - (total * 0.15)
                elif boletos >= 3:
                    total = total - (total * 0.10)

                if tarjeta == 'Si':
                    total = total - (total * 0.10)

                valorPagar = round(total, 2)
                mensaje = 'Compra realizada por: ' + nombre

                venta = {
                    'nombre': nombre,
                    'cantidadCompradores': compradores,
                    'tarjetaCineco': tarjeta,
                    'cantidadBoletos': boletos,
                    'valorPagar': valorPagar
                }

                ventas.append(venta)

        except ValueError:
            mensaje = 'Ingresa cantidades válidas.'

    return render_template(
        'cinepolis.html',
        valorPagar=valorPagar,
        mensaje=mensaje,
        nombre=nombre,
        compradores=compradores,
        tarjeta=tarjeta,
        boletos=boletos
    )

@app.route('/registros')
def registros():
    return render_template('registros.html', ventas=ventas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
