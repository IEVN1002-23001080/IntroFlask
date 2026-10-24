
from flask import Blueprint, jsonify, request
from database import mysql

alumnos_bp = Blueprint(
    'alumnos',
    __name__,
    url_prefix='/api/alumnos'
)


def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


def leer_alumno(matricula):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT * FROM alumnos WHERE matricula = %s",
        (matricula,)
    )
    datos = cursor.fetchone()
    cursor.close()

    if datos is not None:
        return {
            "matricula": datos[0],
            "nombre": datos[1],
            "apaterno": datos[2],
            "amaterno": datos[3],
            "correo": datos[4]
        }

    return None


@alumnos_bp.route("/", methods=['GET'])
def listar_alumnos():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM alumnos")
        datos = cursor.fetchall()
        alumnos = [fila_a_diccionario(cursor, fila) for fila in datos]

        return jsonify({
            'alumnos': alumnos,
            'mensaje': 'Lista de alumnos',
            'exito': True
        }), 200

    except Exception as e:
        return jsonify({
            'mensaje': 'Error al consultar los alumnos',
            'error': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@alumnos_bp.route("/", methods=['POST'])
def registrar_alumno():
    cursor = None
    try:
        datos = request.get_json()

        alumno = leer_alumno(datos['matricula'])

        if alumno is not None:
            return jsonify({
                'alumno': alumno,
                'mensaje': 'El alumno ya existe',
                'exito': False
            }), 409

        cursor = mysql.connection.cursor()
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

        mysql.connection.commit()
        cursor.close()
        cursor = None

        alumno = leer_alumno(datos['matricula'])

        return jsonify({
            'alumno': alumno,
            'mensaje': 'Alumno registrado',
            'exito': True
        }), 201

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': 'Error al registrar el alumno',
            'error': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@alumnos_bp.route("/<matricula>", methods=['GET'])
def consultar_alumno(matricula):
    try:
        alumno = leer_alumno(matricula)

        if alumno is not None:
            return jsonify({
                'alumno': alumno,
                'mensaje': 'Alumno encontrado',
                'exito': True
            }), 200

        return jsonify({
            'mensaje': 'Alumno no encontrado',
            'exito': False
        }), 404

    except Exception as e:
        return jsonify({
            'mensaje': 'Error al consultar el alumno',
            'error': str(e),
            'exito': False
        }), 500


@alumnos_bp.route("/<matricula>", methods=['PUT'])
def actualizar_alumno(matricula):
    cursor = None
    try:
        alumno = leer_alumno(matricula)

        if alumno is None:
            return jsonify({
                'mensaje': 'Alumno no encontrado',
                'exito': False
            }), 404

        datos = request.get_json()

        cursor = mysql.connection.cursor()
        sql = """UPDATE alumnos
                 SET nombre = %s, apaterno = %s,
                 amaterno = %s, correo = %s
                 WHERE matricula = %s"""

        cursor.execute(sql, (
            datos['nombre'],
            datos['apaterno'],
            datos['amaterno'],
            datos['correo'],
            matricula
        ))

        mysql.connection.commit()
        cursor.close()
        cursor = None

        alumno = leer_alumno(matricula)

        return jsonify({
            'alumno': alumno,
            'mensaje': 'Alumno actualizado',
            'exito': True
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': 'Error al actualizar el alumno',
            'error': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@alumnos_bp.route("/<matricula>", methods=['DELETE'])
def eliminar_alumno(matricula):
    cursor = None
    try:
        alumno = leer_alumno(matricula)

        if alumno is None:
            return jsonify({
                'mensaje': 'Alumno no encontrado',
                'exito': False
            }), 404

        cursor = mysql.connection.cursor()
        cursor.execute(
            "DELETE FROM alumnos WHERE matricula = %s",
            (matricula,)
        )

        mysql.connection.commit()

        return jsonify({
            'alumno': alumno,
            'mensaje': 'Alumno eliminado',
            'exito': True
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': 'Error al eliminar el alumno',
            'error': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
