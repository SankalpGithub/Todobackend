import bcrypt

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(hashed_password, input_password):
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)
