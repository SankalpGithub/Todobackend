import random

def generate_otp(length=4):
    """Generate a random OTP of the specified length."""
    otp = ""
    for _ in range(length):
        otp += str(random.randint(0, 9))
    return otp