import secrets

def generate_tracking_number(prefix: str = "TR") -> str:
    # 10 hex chars => 20 chars max avec prefix, simple et lisible
    return prefix + secrets.token_hex(5).upper()
