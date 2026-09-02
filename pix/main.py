from classes import PixKeyRequest
from pix_validator import validate_pix

pix_request = PixKeyRequest(cpf = '56139008840', email = 'kavhsao@gmail.com', cellphone='+5511961394309')
valid_pix: PixKeyRequest = validate_pix(pix_request).model_dump()

print(valid_pix)