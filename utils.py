import pandas as pd

def extract_digits_with_limit_length(chaine):
    try:
        chiffres = ''.join(caractere for caractere in chaine if caractere.isdigit())
    except:
        return None
    return chiffres.strip() if len(chiffres.strip()) > 8 else None

def format_to_desired_pattern(digits):
    try:
        if not digits[0] in ("6", "7"):
            return format_to_desired_pattern(digits[1:])
        else:
            return "0" + digits
    except:
        return None
    
def correct_number(phone_number):
    return (phone_number.startswith(("06", "07")) and len(phone_number) == 10) if not pd.isna(phone_number) else False