from passlib.context import CryptContext

# Initialize password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Function to verify the plain password against the hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Function to hash the plain password using bcrypt algorithm"""
    return pwd_context.hash(password)
