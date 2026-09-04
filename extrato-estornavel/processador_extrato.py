from dataclasses import dataclass

class SaldoInsuficienteError(Exception):
    pass

@dataclass
class Transacao:
    id: str
    valor: float
    tipo: str
    status: str = "CONCLUIDO"

def depositar(transacoes: list[Transacao], id: str, valor: float) -> list[Transacao]:
    transacoes.append(Transacao(id=id, valor=valor, tipo="CREDITO"))
    return transacoes

def sacar(transacoes: list[Transacao], id: str, valor: float) -> list[Transacao]:
    saldo_atual = calcular_saldo(transacoes)
    
    if saldo_atual - valor < 0:
        raise SaldoInsuficienteError("Saldo insuficiente")

    transacoes.append(Transacao(id=id, valor=valor, tipo="DEBITO"))
    return transacoes

def estornar(transacoes: list[Transacao], id_transacao: str) -> list[Transacao]:
    for transacao in transacoes:
        if transacao.id == id_transacao:
            if transacao.status != "CONCLUIDO":
                raise ValueError("Transacao nao pode ser estornada")

            transacao.status = "ESTORNADO"
            return transacoes

    raise ValueError("Transacao nao encontrada")

def calcular_saldo(transacoes: list[Transacao]) -> float:
    saldo = 0.0

    for transacao in transacoes:
        if transacao.status != "CONCLUIDO":
            continue

        if transacao.tipo == "CREDITO":
            saldo += transacao.valor
        elif transacao.tipo == "DEBITO":
            saldo -= transacao.valor

    return saldo