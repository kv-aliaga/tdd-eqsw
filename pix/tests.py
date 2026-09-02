import unittest
from unittest.mock import patch

from email_validator import EmailNotValidError
from phonenumbers import NumberParseException, PhoneNumberType

from classes import InvalidPixKeyError, PixKeyRequest
from pix_validator import (
    _normalize,
    _validate_cellphone,
    _validate_cpf,
    _validate_email,
    validate_pix,
)


class NormalizeTests(unittest.TestCase):
    def test_removes_non_numeric_characters(self):
        self.assertEqual(_normalize("529.982.247-25"), "52998224725")


class CpfValidationTests(unittest.TestCase):
    def test_accepts_valid_cpf_with_formatting(self):
        _validate_cpf("529.982.247-25")

    def test_rejects_cpf_with_invalid_length(self):
        with self.assertRaisesRegex(InvalidPixKeyError, "valid length"):
            _validate_cpf("123")

    def test_rejects_cpf_with_invalid_check_digits(self):
        with self.assertRaisesRegex(InvalidPixKeyError, "not valid"):
            _validate_cpf("111.111.111-11")


class EmailValidationTests(unittest.TestCase):
    @patch("pix_validator.validate_email")
    def test_accepts_valid_email(self, validate_email_mock):
        _validate_email("usuario@example.com")

        validate_email_mock.assert_called_once_with(
            "usuario@example.com", check_deliverability=True
        )

    @patch("pix_validator.validate_email")
    def test_converts_email_library_error_to_domain_error(self, validate_email_mock):
        validate_email_mock.side_effect = EmailNotValidError("invalid domain")

        with self.assertRaisesRegex(InvalidPixKeyError, "e-mail is not valid"):
            _validate_email("usuario@invalido")


class CellphoneValidationTests(unittest.TestCase):
    def test_rejects_cellphone_outside_expected_format(self):
        with self.assertRaisesRegex(InvalidPixKeyError, "valid format"):
            _validate_cellphone("11999999999")

    @patch("pix_validator.number_type", return_value=PhoneNumberType.MOBILE)
    @patch("pix_validator.is_valid_number", return_value=True)
    @patch("pix_validator.parse")
    def test_accepts_valid_mobile_number(self, parse_mock, _, __):
        _validate_cellphone("+5511999999999")

        parse_mock.assert_called_once_with("+5511999999999", "BR")

    @patch("pix_validator.parse", side_effect=NumberParseException(0, "invalid"))
    def test_converts_phone_parser_error_to_domain_error(self, _):
        with self.assertRaisesRegex(InvalidPixKeyError, "cellphone number parsing"):
            _validate_cellphone("+5511999999999")


class PixValidationTests(unittest.TestCase):
    @patch("pix_validator._validate_cellphone")
    @patch("pix_validator._validate_email")
    @patch("pix_validator._validate_cpf")
    def test_validates_all_pix_key_fields(self, cpf_mock, email_mock, cellphone_mock):
        pix = PixKeyRequest(
            cpf="529.982.247-25",
            email="usuario@example.com",
            cellphone="+5511999999999",
        )

        self.assertIsNone(validate_pix(pix))

        cpf_mock.assert_called_once_with(pix.cpf)
        email_mock.assert_called_once_with(pix.email)
        cellphone_mock.assert_called_once_with(pix.cellphone)

    @patch("pix_validator._validate_cpf", side_effect=InvalidPixKeyError("CPF invalido"))
    def test_prints_error_message_when_a_field_is_invalid(self, _):
        pix = PixKeyRequest(
            cpf="123",
            email="usuario@example.com",
            cellphone="+5511999999999",
        )

        with patch("builtins.print") as print_mock:
            self.assertIsNone(validate_pix(pix))

        print_mock.assert_any_call("Message: CPF invalido")


if __name__ == "__main__":
    unittest.main()