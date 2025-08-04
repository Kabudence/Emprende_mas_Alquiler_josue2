from werkzeug.security import generate_password_hash

password_original = "123"
hashed = generate_password_hash(password_original)
print("Password original:", password_original)
print("Password hasheada para MySQL:", hashed)