import requests  # Importa la biblioteca requests para hacer peticiones HTTP

def obtener_credenciales():
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    return username, password

def crear_usuario(nombre, auth):
    url = 'http://localhost:5000/usuarios'
    respuesta = requests.post(url, json={"nombre": nombre}, auth=auth)
    
    if respuesta.status_code == 201:  # Código 201 indica que el recurso fue creado
        print("Usuario creado:", respuesta.json())
    else:
        print("Error al crear usuario:", respuesta.json())

def obtener_usuarios(auth):
    # Realiza una petición GET al servidor
    response = requests.get('http://localhost:5000/usuarios', auth=auth)
    
    if response.status_code == 200:  # Si la respuesta es exitosa (código 200)
        usuarios = response.json()  # Convierte el cuerpo de la respuesta JSON a un objeto de Python (lista de diccionarios)
        print("Usuarios encontrados:")
        for usuario in usuarios:  # Itera sobre la lista de usuarios y muestra sus datos
            print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al obtener usuarios:", respuesta.json())  # Muestra un mensaje de error si la solicitud falla

def eliminar_usuario(usuario_id, auth):
    url = f'http://localhost:5000/usuarios/{usuario_id}'
    respuesta = requests.delete(url, auth=auth)
    
    if respuesta.status_code == 200:  # Código 200 indica que la eliminación fue exitosa
        print(f"Usuario con ID {usuario_id} eliminado.")
    else:
        print("Error al eliminar usuario:", respuesta.json())

if __name__ == '__main__':
    # Obtener credenciales del usuario
    username, password = obtener_credenciales()
    auth = (username, password)

    # Validar credenciales haciendo una petición de prueba
    response = requests.get('http://localhost:5000/quien-soy', auth=auth)
    
    if response.status_code == 200:
        print("Autenticación exitosa.")
        
        # Crear un nuevo usuario
        crear_usuario("Nuevo Usuario", auth)  # Cambia el nombre según necesites
        
        # Obtener y mostrar todos los usuarios
        obtener_usuarios(auth)
        
        # Eliminar un usuario por ID
        eliminar_usuario(3, auth)  
        
        # Volver a obtener y mostrar todos los usuarios
        obtener_usuarios(auth)
    else:
        print("Usuario o contraseña no válidos.")
