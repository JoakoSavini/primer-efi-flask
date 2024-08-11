# EFI FLASK

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
- contar con las instalaciones necesarias: Flask, Flask-SQLAlchemy, Flask-Migrate y PyMySQL
  codigo de consola: pip install Flask Flask-SQLAlchemy Flask-Migrate PyMySQL
- se debe inicializar en consola el siguiente codigo: "flask init-db". Esto sirve para que la base de datos cuente con valores predeterminados ya listos para usar.

### Manual de Uso
__Para que el sistema funcione se debe respetar el siguiente orden de carga:__
1- Marca
2- Modelo
3- Fabricante
4- Proveedor
5- Celular
