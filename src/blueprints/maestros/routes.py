
from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)


def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


def leer_maestro(id_maestro):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT * FROM maestros WHERE id_maestro = %s",
        (id_maestro,)
    )
    datos = cursor.fetchone()
    cursor.close()

    if datos is not None:
        return {
            "id_maestro": datos[0],
            "nombre": datos[1],
            "apaterno": datos[2],
            "amaterno": datos[3],
            "correo": datos[4]
        }

    return None


@maestros_bp.route("/", methods=['GET'])
def listar_maestros():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM maestros")
        datos = cursor.fetchall()
        maestros = [fila_a_diccionario(cursor, fila) for fila in datos]

        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200

    except Exception as e:
        return jsonify({
            'mensaje': 'Error al consultar los maestros',
            'error': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@maestros_bp.route("/", methods=['POST'])
def registrar_maestro():
    cursor = None
    try:
        datos = request.get_json()

        cursor = mysql.connection.cursor()
        sql = """INSERT INTO maestros
                 (nombre, apaterno, amaterno, correo)
                 VALUES (%s, %s, %s, %s)"""

        cursor.execute(sql, (
            datos['nombre'],
            datos['apaterno'],
            datos['amaterno'],
            datos['correo']
        ))

        id_maestro = cursor.lastrowid
        mysql.connection.commit()
        cursor.close()
        cursor = None

        maestro = leer_maestro(id_maestro)

        return jsonify({
            'maestro': maestro,
            'mensaje': 'Maestro registrado',
            'exito': True
        }), 201

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': 'Error al registrar el maestro',
            'error': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@maestros_bp.route("/<int:id_maestro>", methods=['GET'])
def consultar_maestro(id_maestro):
    try:
        maestro = leer_maestro(id_maestro)

        if maestro is not None:
            return jsonify({
                'maestro': maestro,
                'mensaje': 'Maestro encontrado',
                'exito': True
            }), 200

        return jsonify({
            'mensaje': 'Maestro no encontrado',
            'exito': False
        }), 404

    except Exception as e:
        return jsonify({
            'mensaje': 'Error al consultar el maestro',
            'error': str(e),
            'exito': False
        }), 500


@maestros_bp.route("/<int:id_maestro>", methods=['PUT'])
def actualizar_maestro(id_maestro):
    cursor = None
    try:
        maestro = leer_maestro(id_maestro)

        if maestro is None:
            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            }), 404

        datos = request.get_json()

        cursor = mysql.connection.cursor()
        sql = """UPDATE maestros
                 SET nombre = %s, apaterno = %s,
                 amaterno = %s, correo = %s
                 WHERE id_maestro = %s"""

        cursor.execute(sql, (
            datos['nombre'],
            datos['apaterno'],
            datos['amaterno'],
            datos['correo'],
            id_maestro
        ))

        mysql.connection.commit()
        cursor.close()
        cursor = None

        maestro = leer_maestro(id_maestro)

        return jsonify({
            'maestro': maestro,
            'mensaje': 'Maestro actualizado',
            'exito': True
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': 'Error al actualizar el maestro',
            'error': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@maestros_bp.route("/<int:id_maestro>", methods=['DELETE'])
def eliminar_maestro(id_maestro):
    cursor = None
    try:
        maestro = leer_maestro(id_maestro)

        if maestro is None:
            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            }), 404

        cursor = mysql.connection.cursor()
        cursor.execute(
            "DELETE FROM maestros WHERE id_maestro = %s",
            (id_maestro,)
        )

        mysql.connection.commit()

        return jsonify({
            'maestro': maestro,
            'mensaje': 'Maestro eliminado',
            'exito': True
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': 'Error al eliminar el maestro',
            'error': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
