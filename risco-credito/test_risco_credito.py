# 	Motor de Análise de Risco de Crédito (Score Interno)
#   Objetivo: Construir a lógica de avaliação automática de limite de cartão de crédito com base no perfil financeiro do cliente.

# 	Regras de Negócio:
# 	Regra 1: Renda mensal < R$ 1.500,00 → Limite aprovado: R$ 0,00 (Crédito negado).
# 	Regra 2: Se o cliente possui restrições no CPF (nome sujo) → Limite aprovado: R$ 0,00 independente da renda.
# 	Regra 3: Se renda ≥ R$ 1.500,00 sem restrições → Limite inicial base = 30% da renda mensal.
# 	Regra 4: Se o score externo for acima de 800 → Aplica um bônus de +50% sobre o limite inicial base.
# 	Desafio TDD: Usar parametrização de testes (@pytest.mark.parametrize) para testar múltiplas combinações de renda, restrição e score com poucas linhas de teste.


import pytest
from risco_credito import calcular_limite_credito

@pytest.mark.parametrize("renda, possui_restricao, score, limite_esperado", [

    # 1 - Renda abaixo do mínimo
    (1499.99, False, 900, 0.0),
    
    # 2 - Possui restrição no CPF
    (5000.0, True, 850, 0.0),
    
    # 3 - Renda válida sem restrição e score <= 800 (30% da renda)
    (2000.0, False, 750, 600.0),
    
    # 4 - Renda válida sem restrição e score > 800 (30% da renda + 50% de bônus)
    (2000.0, False, 801, 900.0),
    (3000.0, False, 850, 1350.0),
])

def test_calcular_limite_credito(renda, possui_restricao, score, limite_esperado):

    limite = calcular_limite_credito(renda, possui_restricao, score)
    
    assert limite == pytest.approx(limite_esperado)