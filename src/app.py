
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])

con = MySQL(app)
CORS(app)


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>", 404


@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    cursor = None

    try:
        cursor = con.connection.cursor()

        sql = "SELECT * FROM alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()

        alumnos = []

        for fila in datos:
            alumno = {
                "matricula": fila[0],
                "nombre": fila[1],
                "apaterno": fila[2],
                "amaterno": fila[3],
                "correo": fila[4]
            }

            alumnos.append(alumno)

        return jsonify({
            'alumnos': alumnos,
            'mensaje': 'Lista de alumnos',
            'exito': True
        })

    except Exception as ex:
        app.logger.exception("Error al consultar alumnos")
        return jsonify({
            "message": "error {}".format(ex),
            "exito": False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
