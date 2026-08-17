import secrets

def _check_digit(first14: str) -> str:
    total = 0
    for idx, ch in enumerate(first14, start=1):
        n = int(ch)
        if idx % 2 == 0:
            n *= 2
            n = n // 10 + n % 10
        total += n
    return str((10 - total % 10) % 10)

def validate_imei(imei: str):
    if not isinstance(imei, str) or len(imei) != 15 or not imei.isdigit():
        return False, "IMEI must contain exactly 15 numeric digits."
    if imei[-1] != _check_digit(imei[:14]):
        return False, "IMEI check digit is invalid."
    return True, "VALID"

def generate_valid_imei() -> str:
    first14 = "99" + "".join(str(secrets.randbelow(10)) for _ in range(12))
    return first14 + _check_digit(first14)
