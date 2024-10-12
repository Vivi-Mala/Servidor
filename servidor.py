from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Base de datos simulada
base_datos = {
    "usuarios": [
        {"id": 1, "nombre": "Yuri"},
        {"id": 2, "nombre": "Viviana"}
    ]
}

# Usuarios permitidos con autenticación básica (se recomienda no almacenarlos en texto plano)
usuarios_permitidos = {
    "admin": generate_password_hash("admin123"),
    "user": generate_password_hash("user123")
}

# Función para verificar las credenciales
@auth.verify_password
def verificar_password(username, password):
    if username in usuarios_permitidos and check_password_hash(usuarios_permitidos[username], password):
        return username
    return None

# Ruta pública para obtener usuarios (no requiere autenticación)
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(base_datos["usuarios"])  # Devuelve la lista de usuarios en formato JSON

# Ruta protegida por autenticación básica para crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
@auth.login_required
def crear_usuario():
    nuevo_usuario = request.get_json()  # Obtiene los datos enviados en la solicitud POST
    if not nuevo_usuario or not "nombre" in nuevo_usuario:  # Valida que el nombre esté presente
        return jsonify({"error": "El nombre es requerido"}), 400
    
    nombre = nuevo_usuario["nombre"]
    if len(nombre.strip()) == 0:
        return jsonify({"error": "El nombre no puede estar vacío"}), 400
    elif len(nombre) < 3:
        return jsonify({"error": "El nombre debe tener al menos 3 caracteres"}), 400

    # Asignación automática de un nuevo ID
    nuevo_usuario["id"] = len(base_datos["usuarios"]) + 1
    base_datos["usuarios"].append(nuevo_usuario)  # Agrega el nuevo usuario a la base de datos simulada

    return jsonify(nuevo_usuario), 201  # Responde con el nuevo usuario creado y el código 201 (Created)

# Ruta protegida por autenticación básica para eliminar un usuario por ID
@app.route('/usuarios/<int:id>', methods=['DELETE'])
@auth.login_required
def eliminar_usuario(id):
    usuario = next((u for u in base_datos["usuarios"] if u["id"] == id), None)  # Busca el usuario por ID
    
    if usuario is None:  # Si el usuario no existe, devuelve un error
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    base_datos["usuarios"].remove(usuario)  # Elimina el usuario de la base de datos simulada
    return jsonify({"mensaje": f"Usuario con ID {id} eliminado"}), 200  # Responde con un mensaje de éxito

# Ruta protegida para obtener el nombre del usuario autenticado
@app.route('/quien-soy', methods=['GET'])
@auth.login_required
def quien_soy():
    return jsonify({"usuario": auth.current_user()})  # Devuelve el nombre de usuario autenticado

if __name__ == '__main__':
    app.run(port=5000)  # Ejecuta el servidor en el puerto 5000
