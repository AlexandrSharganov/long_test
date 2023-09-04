import random

def generate_otp_code():
    otp_length = 6
    otp_digits = '0123456789'

    otp_code = ''.join(random.choice(otp_digits) for _ in range(otp_length))
    return otp_code