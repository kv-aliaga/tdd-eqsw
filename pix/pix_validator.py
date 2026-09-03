from classes import PixKeyRequest, InvalidPixKeyError
from email_validator import EmailNotValidError
from re import sub, match
from validate_docbr import CPF
from email_validator import validate_email
from phonenumbers import number_type, parse, is_valid_number, PhoneNumberType, NumberParseException
from re import sub

def validate_pix(pix: PixKeyRequest) -> PixKeyRequest:
    try:
        _validate_cpf(pix.cpf)
        _validate_email(pix.email)
        _validate_cellphone(pix.cellphone)

        return pix
    except InvalidPixKeyError as ipke:
        print(f'Message: {ipke.message}')
        print(f'Timestamp: {ipke.timestamp}')

def _validate_cpf(cpf: str):
    cpf = sub(r'\D', '', cpf)

    if len(cpf) != 11:
        raise InvalidPixKeyError('The provided CPF does not have a valid length.')

    if not CPF().validate(cpf):
        raise InvalidPixKeyError('The provided CPF is not valid')    

def _validate_email(email: str):
    try:
        validate_email(email, check_deliverability=True)
    except EmailNotValidError as enve:
        raise InvalidPixKeyError(f'The provided e-mail is not valid. {enve}')

def _validate_cellphone(cellphone: str):
    if not match(r'^\+55\d{2}9\d{8}$', cellphone):
        raise InvalidPixKeyError('The provided cellphone is not in a valid format')
    
    try:
        parsed = parse(cellphone, 'BR')
        is_valid = is_valid_number(parsed)
        is_mobile = number_type(parsed) == PhoneNumberType.MOBILE

        if not is_valid and not is_mobile:
            raise InvalidPixKeyError('The provided cellphone does not exist')
    except NumberParseException:
        raise InvalidPixKeyError('There was a error during the cellphone number parsing')