def calcular_limite_credito(renda: float, possui_restricao: bool, score: int) -> float:

    # Renda insuficiente ou restrição no CPF
    if renda < 1500.0 or possui_restricao:
        return 0.0

    # Limite base de 30% da renda
    limite_base = renda * 0.30

    # Bônus de 50% sobre o limite base se score > 800
    if score > 800:
        limite_base *= 1.50

    return limite_base