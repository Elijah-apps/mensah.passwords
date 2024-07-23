import random
import string

def generate_password(length=12, include_symbols=True, include_numbers=True, include_uppercase=True, include_lowercase=True):
    characters = ""
    if include_symbols:
        characters += string.punctuation
    if include_numbers:
        characters += string.digits
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    
    if not characters:
        raise ValueError("At least one character type must be selected")

    password = ''.join(random.choice(characters) for i in range(length))
    return password
