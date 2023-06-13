import http
import json

import allure

from consts import Filenames, Encodings, Test_Data_Keys as Keys
from data_models import ValidResponseReverse, ErrorResponse
from utils import json_utils


@allure.feature("Тестирование обратного геокодирования")
class Test_Reverse_Geocoding:

    @allure.story("Позитивные тесты - проверка валидности ответов на корректные запросы")
    def test_valid(self, valid_response, req_params_valid, valid_expected, get_logger):
        with allure.step("Проверка кода статуса ответа"):
            get_logger.info(f"Проверка кода статуса ответа - ожидаемый код {http.HTTPStatus.OK}")
            assert valid_response.status_code == http.HTTPStatus.OK, \
                f"Неверный код ответа, получен {valid_response.status_code}"
        with allure.step("Проверка валидности JSON схемы тела ответа"):
            with open(Filenames.SCHEMA_REVERSE_CODING, "r", encoding=Encodings.UTF8) as schema_file:
                get_logger.info(f"Проверка тела ответа на соответствие JSON схеме из файла {schema_file.name}")
                assert json_utils.validate_schema(valid_response.json(),
                                                  json.load(schema_file)), "Неверная JSON схема ответа"
        with allure.step("Проверка соответствия первого результата из тела ответа ожидаемому"):
            expected_response = ValidResponseReverse(display_name=valid_expected[Keys.DISPLAY_NAME],
                                                     city=valid_expected[Keys.CITY],
                                                     country=valid_expected[Keys.COUNTRY],
                                                     lat=req_params_valid[0], lon=req_params_valid[1],
                                                     rel_tol=valid_expected[Keys.REL_TOL])
            actual_response = ValidResponseReverse(display_name=valid_response.json()[Keys.DISPLAY_NAME],
                                                   city=valid_response.json()[Keys.ADDRESS][Keys.CITY],
                                                   country=valid_response.json()[Keys.ADDRESS][Keys.COUNTRY],
                                                   lat=valid_response.json()[Keys.LAT],
                                                   lon=valid_response.json()[Keys.LON])
            get_logger.info(f"Проверка корректности тела ответа {valid_response.json()}")
            assert actual_response == expected_response, "Некорректное тело ответа"

    @allure.story("Негативные тесты (в запросе пропущены координаты)")
    def test_empty_fields(self, empty_fields_response, empty_fields_expected, get_logger):
        get_logger.info(f"Проверка кода статуса ответа - ожидаемый код {http.HTTPStatus.BAD_REQUEST}")
        with allure.step("Проверка кода статуса ответа"):
            assert empty_fields_response.status_code == http.HTTPStatus.BAD_REQUEST, \
                f"Неверный код ответа, получен {empty_fields_response.status_code}"
        with allure.step("Проверка валидности JSON схемы тела ответа"):
            with open(Filenames.SCHEMA_CODING_ERROR, "r", encoding=Encodings.UTF8) as schema_file:
                get_logger.info(f"Проверка тела ответа на соответствие JSON схеме из файла {schema_file.name}")
                assert json_utils.validate_schema(empty_fields_response.json(),
                                                  json.load(schema_file)), "Неверная JSON схема ответа"
        with allure.step("Проверка корректности тела ответа"):
            get_logger.info("Проверка полей тела ответа code, message на соответствие ожидаемым")
            expected_response = ErrorResponse(code=empty_fields_expected[Keys.CODE],
                                              message=empty_fields_expected[Keys.MESSAGE])
            actual_response = ErrorResponse(code=empty_fields_response.json()[Keys.ERROR][Keys.CODE],
                                            message=empty_fields_response.json()[Keys.ERROR][Keys.MESSAGE])
            get_logger.info(f"Проверка корректности тела ответа {empty_fields_response.json()}")
            assert expected_response == actual_response, "Некорректное тело ответа"

    @allure.story("Негативные тесты (невалидные значения координат)")
    def test_invalid_coords(self, invalid_coords_response, invalid_coords_expected, get_logger):
        get_logger.info(f"Проверка кода статуса ответа - ожидаемый код {http.HTTPStatus.BAD_REQUEST}")
        with allure.step("Проверка кода статуса ответа"):
            assert invalid_coords_response.status_code == http.HTTPStatus.BAD_REQUEST, \
                f"Неверный код ответа, получен {invalid_coords_response.status_code}"
        with allure.step("Проверка валидности JSON схемы тела ответа"):
            with open(Filenames.SCHEMA_CODING_ERROR, "r", encoding=Encodings.UTF8) as schema_file:
                get_logger.info(f"Проверка тела ответа на соответствие JSON схеме из файла {schema_file.name}")
                assert json_utils.validate_schema(invalid_coords_response.json(),
                                                  json.load(schema_file)), "Неверная JSON схема ответа"
        with allure.step("Проверка корректности тела ответа"):
            get_logger.info("Проверка полей тела ответа code, message на соответствие ожидаемым")
            expected_response = ErrorResponse(code=invalid_coords_expected[Keys.CODE],
                                              message=invalid_coords_expected[Keys.MESSAGE])
            actual_response = ErrorResponse(code=invalid_coords_response.json()[Keys.ERROR][Keys.CODE],
                                            message=invalid_coords_response.json()[Keys.ERROR][Keys.MESSAGE])
            get_logger.info(f"Проверка корректности тела ответа {invalid_coords_response.json()}")
            assert expected_response == actual_response, "Некорректное тело ответа"

    @allure.story("Негативные тесты (слишком большой размер параметров запроса)")
    def test_too_large_params(self, too_large_params_response, get_logger):
        with allure.step("Проверка кода статуса ответа"):
            get_logger.info(f"Проверка кода статуса ответа - ожидаемый код {http.HTTPStatus.REQUEST_URI_TOO_LONG}")
            assert too_large_params_response.status_code == http.HTTPStatus.REQUEST_URI_TOO_LONG, \
                f"Неверный код ответа, получен {too_large_params_response.status_code}"
