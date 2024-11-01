from werkzeug.security import generate_password_hash

# Define la nueva contraseña
nueva_contrasena = "admin"

# Genera el hash
hashed_password = generate_password_hash(nueva_contrasena)

# Muestra el hash
print("Hash de la nueva contraseña:", hashed_password)
