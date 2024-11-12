# EFI FLASK (Parte 1)

### Idea del trabajo
__crear un sistema para un local de venta de celulares__ 

### Funcionalidades
__EL sistema debe:__
- Respetar el CRUD (Create, Read, Update, Delete)
- Contar con, al menos, 8 modelos
- Contar con una Base de Datos creada en LocalHost

### Requerimientos
__Para un correcto funcionamiento del codigo se debe:__
- contar con un entorno virtual, de preferencia llamado "ent" para que el .gitignore lo tome y evitar problemas en caso de edición de código
- contar con las instalaciones necesarias: Flask, Flask-SQLAlchemy, Flask-Migrate y PyMySQL (todo en los requirements.txt)
- se debe inicializar en consola el siguiente codigo: "flask init-db". Esto sirve para que la base de datos cuente con valores predeterminados ya listos para usar.

### Manual de Uso
__Para que el sistema funcione se debe respetar el siguiente orden de carga:__
- 1- Marca
- 2- Modelo
- 3- Fabricante
- 4- Proveedor
- 5- Celular

# EFI FLASK (Parte 2)

### Idea del Trabajo

__crear una API que permita la autenticacion y gestion de usuarios con roles de acceso(admin y usuario regular) donde solo los administradores puedan crear, actualizar y eliminar usuarios, modelos, marcas, celulares, etc; mientras que todos los usuarios "regulares" autenticados pueden ver la lista de cada modelo.__

### Instalacion

- 1- Clonar el repositorio:
```bash
git clone https://github.com/JoakoSavini/primer-efi-flask.git
cd primer-efi-flask
```
- 2- Instalar Dependencias
```bash
pip install -r requirements.txt
```
- 3- Ejecutar Aplicacion
```bash
flask run --reload
```
### Endpoints
__Login(POST/login)__
Este endpoint permite a los usuarios autenticarse con su username y password, generando un token para las siguientes solicitudes.
- Endpoint: /api/login/
- Metodo: POST
- Cuerpo de la Solicitud:
```bash
{
    "username": "admin",
    "password": "admin"
}
```
- Ejemplo de respuesta:
```bash
{
    "token": "Bearer <token>"
}
```
- Error: - Codigo 401 si las credenciales son incorrectas.

__Usuarios(GET/users)__
Devuelve una lista de todos los usuarios. Los administradores verán detalles completos de los usuarios, mientras que los usuarios regulares verán solo información básica.
- Endpoint: /api/users/
- Metodo: GET
- Cabecera de la solicitud: Authorization: Token <tu_token_de_autenticacion>
- Ejemplo de respuesta:
    - si el usuario es admin
    ```bash
    [
        {
            "id": 1,
            "username": "usuario1",
            "is_admin": false
        }
    ]
    ```
    - si el usuario es "regular":
    ```bash
    [
        {
            "username": "usuario1"
        }
    ]
    ```




