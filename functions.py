import hashlib, random


#зашифровка пароля
def hash_password(password):
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password

#создание рандомного числа 
def generate_random_number():
    number = random.randint(10000, 99999)
    return number