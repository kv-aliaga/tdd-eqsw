import pytest

from processador_extrato import (
    SaldoInsuficienteError,
    calcular_saldo,
    depositar,
    estornar,
    sacar,
)


def test_deve_calcular_saldo_com_creditos_e_debitos():
    transacoes = []
    depositar(transacoes, "1", 1000.0)
    sacar(transacoes, "2", 300.0)
    depositar(transacoes, "3", 200.0)

    assert calcular_saldo(transacoes) == pytest.approx(900.0)


def test_nao_deve_permitir_saque_que_deixe_saldo_negativo():
    transacoes = []
    depositar(transacoes, "1", 100.0)

    with pytest.raises(SaldoInsuficienteError):
        sacar(transacoes, "2", 150.0)


def test_deve_estornar_transacao_concluida_e_recalcular_saldo():
    transacoes = []
    depositar(transacoes, "1", 1000.0)
    sacar(transacoes, "2", 200.0)
    estornar(transacoes, "2")

    assert calcular_saldo(transacoes) == pytest.approx(1000.0)
    assert transacoes[1].status == "ESTORNADO"


def test_deve_mantener_historico_final_de_operacoes_complexas():
    transacoes = []
    depositar(transacoes, "1", 1000.0)
    sacar(transacoes, "2", 200.0)
    depositar(transacoes, "3", 150.0)
    sacar(transacoes, "4", 300.0)
    estornar(transacoes, "4")
    depositar(transacoes, "5", 50.0)

    assert calcular_saldo(transacoes) == pytest.approx(1000.0)
    assert [t.id for t in transacoes] == ["1", "2", "3", "4", "5"]
    assert [t.status for t in transacoes] == ["CONCLUIDO", "CONCLUIDO", "CONCLUIDO", "ESTORNADO", "CONCLUIDO"]
