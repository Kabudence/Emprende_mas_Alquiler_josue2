from werkzeug.security import generate_password_hash

password_original = "hashed_password_here"
hashed = generate_password_hash(password_original)
print("Password original:", password_original)
print("Password hasheada para MySQL:", hashed)
