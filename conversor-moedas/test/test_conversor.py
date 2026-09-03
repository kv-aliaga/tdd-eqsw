from unittest.mock import Mock

from cotacao_api import CotacaoAPI, Moeda
from conversor_moedas import ConversorMoedas


def test_deve_calcular_conversao_base():
    cotacao_api = Mock(spec=CotacaoAPI)
    cotacao_api.obter_taxa.return_value = 5.0
    conversor = ConversorMoedas(cotacao_api)

    resultado = conversor.calcular_conversao_base(Moeda.USD, Moeda.BRL, 100)

    assert resultado == 500.0