
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
 
from config import config
 
app = Flask(__name__)
 
CORS(app)
 
con = MySQL(app)
 
@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno = {"matricula": fila[0], "nombre": fila[1],
                      "apaterno": fila[2], "amaterno": fila[3],
                      "correo": fila[4]}
            alumnos.append(alumno)
        cursor.close()
        return jsonify({'alumnos': alumnos, 'mensaje': 'Lista de alumnos',
                        'exito': True})
 
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False}), 500
 
 
def leer_alumno_bd(matricula):
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM alumnos WHERE matricula = %s"
        cursor.execute(sql, (matricula,))
        datos = cursor.fetchone()
        cursor.close()
 
        if datos is not None:
            alumno = {"matricula": datos[0], "nombre": datos[1],
                      "apaterno": datos[2], "amaterno": datos[3],
                      "correo": datos[4]}
            return alumno
        else:
            return None
    except Exception as ex:
        raise ex
 
@app.route("/alumnos/<mat>", methods=['GET'])
def leer_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno is not None:
            return jsonify({'alumno': alumno,
                            'mensaje': 'Alumno encontrado', 'exito': True})
        else:
            return jsonify({'alumno': alumno,
                            'mensaje': 'Alumno no encontrado', 'exito': False}), 404
 
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False}), 500

@app.route("/alumnos", methods=['POST'])
def registra_alumno():
    try:
        datos = request.get_json()
        alumno = leer_alumno_bd(datos['matricula'])
        if alumno is not None:
            return jsonify({'alumno': alumno,
                            'mensaje': 'Alumno ya existe', 'exito': False}), 409
        else:
            cursor = con.connection.cursor()
            sql = """INSERT INTO alumnos
                     (matricula, nombre, apaterno, amaterno, correo)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                datos['matricula'],
                datos['nombre'],
                datos['apaterno'],
                datos['amaterno'],
                datos['correo']
            ))
            con.connection.commit()
            cursor.close()
            alumno = leer_alumno_bd(datos['matricula'])
            return jsonify({'alumno': alumno,
                            'mensaje': 'Alumno registrado', 'exito': True}), 201
    except Exception as ex:
        con.connection.rollback()
        return jsonify({"message": "error {}".format(ex), 'exito': False}), 500


@app.route("/alumnos/<mat>", methods=['PUT'])
def actualizar_cursor(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno is not None:
            datos = request.get_json()
            cursor = con.connection.cursor()
            sql = """UPDATE alumnos
                     SET nombre = %s, apaterno = %s, amaterno = %s, correo = %s
                     WHERE matricula = %s"""
            cursor.execute(sql, (
                datos['nombre'],
                datos['apaterno'],
                datos['amaterno'],
                datos['correo'],
                mat
            ))
            con.connection.commit()
            cursor.close()
            alumno = leer_alumno_bd(mat)
            return jsonify({'alumno': alumno,
                            'mensaje': 'Alumno actualizado', 'exito': True})
        else:
            return jsonify({'alumno': None,
                            'mensaje': 'Alumno no encontrado', 'exito': False}), 404
    except Exception as ex:
        con.connection.rollback()
        return jsonify({"message": "error {}".format(ex), 'exito': False}), 500
          

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>", 404
 
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)
