from abc import ABC, abstractmethod
from enum import Enum, auto

class Moeda(Enum):
    BRL = auto()
    USD = auto()
    EUR = auto()

class CotacaoAPI(ABC):
    @abstractmethod
    def obter_taxa(self, moeda_origem : Moeda, moeda_destino: Moeda) -> float:
        pass