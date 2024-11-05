from werkzeug.security import generate_password_hash

nueva_contrasena = "admin"
hashed_password = generate_password_hash(nueva_contrasena)
print(hashed_password)