from dataclasses import dataclass, field
from pydantic import BaseModel, Field, field_serializer
from uuid import uuid4
from datetime import datetime
from re import sub

class PixKeyRequest(BaseModel):
    cpf: str
    email: str
    cellphone: str
    random_key: str = Field(default_factory=lambda: str(uuid4()))

    @field_serializer('cpf')
    def format_cpf(self, cpf: str) -> str:
        digits = sub(r'\D', '', cpf)
        return(f'{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}')
    
    @field_serializer('cellphone')
    def format_cellphone(self, cellphone: str) -> str:
        digits = sub(r'\D', '', cellphone)
        return(f'+{digits[:2]} ({digits[2:4]}) {digits[4:9]}-{digits[9:]}')

@dataclass
class InvalidPixKeyError(Exception):
    message: str
    timestamp: str = field(init=False)

    def __post_init__(self):
        super().__init__(self.message)
        self.timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
