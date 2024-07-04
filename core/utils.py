# utils.py
import random


def generate_random_credit_card():
    # Generate the first part of the number (2221xxxx...), ensuring it's 19 digits in total
    first_part = "2221" + ''.join(random.choices('0123456789', k=15))
    # Convert the first part to an integer to ensure it's treated as a number
    number = int(first_part)
    month = random.randint(1, 12)
    year = str(random.randint(2023, 2030))[-2:]
    cvv = random.randint(100, 999)
    card_type = 'mastercard'
    return {
        'number': number,
        'month': month,
        'year': year,
        'cvv': cvv,
        'card_type': card_type
    }
