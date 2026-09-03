from cotacao_api import CotacaoAPI, Moeda

class ConversorMoedas:
    def __init__(self, cotacao_api: CotacaoAPI):
        self.cotacao_api = cotacao_api
    
    def calcular_conversao_base(self, moeda_origem: Moeda, moeda_destino: Moeda, valor: float) -> float:
        taxa = self.cotacao_api.obter_taxa(moeda_origem, moeda_destino)
        valor_convertido = valor * taxa

        return valor_convertido