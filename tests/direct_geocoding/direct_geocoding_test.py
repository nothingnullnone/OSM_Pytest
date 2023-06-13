import http
import json

import allure

from consts import Filenames, Encodings, Test_Data_Keys as Keys
from data_models import ValidResponseDirect, ErrorResponse
from utils import json_utils


@allure.feature("Тестирование прямого геокодирования")
class Test_Direct_Geocoding:

    @allure.story("Позитивные тесты - проверка валидности ответов на корректные запросы")
    def test_valid(self, valid_response, valid_expected, get_logger):
        get_logger.info(f"Проверка кода статуса ответа - ожидаемый код {http.HTTPStatus.OK}")
        with allure.step("Проверка кода статуса ответа"):
            assert valid_response.status_code == http.HTTPStatus.OK, \
                f"Неверный код ответа, получен {valid_response.status_code}"
        with allure.step("Проверка валидности JSON схемы тела ответа"):
            with open(Filenames.SCHEMA_DIRECT_CODING, "r", encoding=Encodings.UTF8) as schema_file:
                get_logger.info(f"Проверка тела ответа на соответствие JSON схеме из файла {schema_file.name}")
                assert json_utils.validate_schema(valid_response.json(),
                                                  json.load(schema_file)), "Неверная JSON схема ответа"
        with allure.step("Проверка соответствия первого результата из тела ответа ожидаемому"):
            expected_response = ValidResponseDirect(lat=valid_expected[Keys.LAT], lon=valid_expected[Keys.LON],
                                                    rel_tol=valid_expected[Keys.REL_TOL])
            actual_response = ValidResponseDirect(lat=valid_response.json()[0][Keys.LAT],
                                                  lon=valid_response.json()[0][Keys.LON])
            get_logger.info(f"Проверка корректности тела ответа {valid_response.json()}")
            assert actual_response == expected_response, "Некорректное тело ответа"

    @allure.story("Негативные тесты (невалидные значения полей запроса)")
    def test_invalid_fields(self, invalid_fields_response, invalid_fields_expected, get_logger):
        with allure.step("Проверка кода статуса ответа"):
            get_logger.info(f"Проверка кода статуса ответа - ожидаемый код {http.HTTPStatus.BAD_REQUEST}")
            assert invalid_fields_response.status_code == http.HTTPStatus.BAD_REQUEST, \
                f"Неверный код ответа, получен {invalid_fields_response.status_code}"
        with allure.step("Проверка валидности JSON схемы тела ответа"):
            with open(Filenames.SCHEMA_CODING_ERROR, "r", encoding=Encodings.UTF8) as schema_file:
                get_logger.info(f"Проверка тела ответа на соответствие JSON схеме из файла {schema_file.name}")
                assert json_utils.validate_schema(invalid_fields_response.json(), json.load(schema_file)), \
                    "Неверная JSON схема ответа"
        with allure.step("Проверка корректности тела ответа"):
            expected_response = ErrorResponse(code=invalid_fields_expected[Keys.CODE],
                                              message=invalid_fields_expected[Keys.MESSAGE])
            actual_response = ErrorResponse(code=invalid_fields_response.json()[Keys.ERROR][Keys.CODE],
                                            message=invalid_fields_response.json()[Keys.ERROR][Keys.MESSAGE])
            get_logger.info(f"Проверка корректности тела ответа {invalid_fields_response.json()}")
            assert actual_response == expected_response, "Некорректное тело ответа"

    @allure.story("Негативные тесты (слишком большой размер параметров запроса)")
    def test_too_large_params(self, too_large_params_response, get_logger):
        get_logger.info(f"Проверка кода статуса ответа - ожидаемый код {http.HTTPStatus.REQUEST_URI_TOO_LONG}")
        with allure.step("Проверка кода статуса ответа"):
            assert too_large_params_response.status_code == http.HTTPStatus.REQUEST_URI_TOO_LONG, \
                f"Неверный код ответа, получен {too_large_params_response.status_code}"
