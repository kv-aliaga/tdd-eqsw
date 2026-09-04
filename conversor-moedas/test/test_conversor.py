import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from cotacao_api import CotacaoAPI, Moeda
from conversor_moedas import ConversorMoedas, ServicoCotacaoIndisponivelError


def test_deve_calcular_conversao_base():
    cotacao_api = Mock(spec=CotacaoAPI)
    cotacao_api.obter_taxa.return_value = 5.0
    conversor = ConversorMoedas(cotacao_api)

    resultado = conversor.calcular_conversao_base(Moeda.USD, Moeda.BRL, 100)

    assert resultado == pytest.approx(507.5)


def test_deve_lancar_erro_quando_api_estiver_indisponivel():
    cotacao_api = Mock(spec=CotacaoAPI)
    cotacao_api.obter_taxa.side_effect = Exception("api fora do ar")
    conversor = ConversorMoedas(cotacao_api)

    with pytest.raises(ServicoCotacaoIndisponivelError):
        conversor.calcular_conversao_base(Moeda.USD, Moeda.BRL, 100)
