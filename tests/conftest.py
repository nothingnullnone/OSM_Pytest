import logging

import allure
import pytest
import requests

from consts import Scopes, Test_Data_Keys as Keys
from utils import random_utils

REQUEST_TIMEOUT = 3


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


@pytest.fixture(scope=Scopes.CLASS, name="get_logger")
def get_logger_fixture():
    return get_logger()


# Общая фикстура для отправки GET запроса
@pytest.fixture(scope=Scopes.CLASS, name="request_get")
def get_request_fixture():
    def _get_request(url, params):
        with allure.step('Выполнение GET запроса к url {url} с параметрами {params}'):
            logger = get_logger()
            logger.info(f'Выполнение GET запроса к url {url} с параметрами {params}')
        return requests.get(url=url, params=params, timeout=REQUEST_TIMEOUT)
    yield _get_request


# Фикстура с общим кодом для отправки запроса с длиной параметров, превышающей допустимую
@pytest.fixture(scope=Scopes.CLASS)
def too_large_params_response(request_get):
    def _too_large_params_response(endpoint, test_data_too_large_params):
        for k in test_data_too_large_params[Keys.REQ_PARAMS]:
            param_len = test_data_too_large_params[Keys.REQ_PARAMS][k][Keys.LEN]
            test_data_too_large_params[Keys.REQ_PARAMS][k] = random_utils.get_random_int(param_len)
        return request_get(url=endpoint, params=test_data_too_large_params[Keys.REQ_PARAMS])
    yield _too_large_params_response


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport():
    outcome = yield
    rep = outcome.get_result()

    # Перехват и логирование результатов тестов - в случае успеха вывод сообщения, в случае упавшего теста - вывод
    # сообщения об ошибке и трейсбека
    if rep.when == "call" and rep.passed:
        allure.attach("Тест успешно пройден", "Результат теста", allure.attachment_type.TEXT)

    if rep.when == "call" and rep.failed:
        allure.attach("Тест не пройден!", "Результат теста", allure.attachment_type.TEXT)
        allure.attach(f"{rep.longrepr.reprcrash.message}", "Exception Message", allure.attachment_type.TEXT)
        allure.attach(f"{rep.longrepr.reprtraceback}", "Traceback", allure.attachment_type.TEXT)

    # Для фикстур нет необходимости логировать успешное завершение, логируются только сломанные фикстуры
    if (rep.when == "setup" or rep.when == "teardown") and rep.failed:
        allure.attach("Тест не пройден! Фикстура сломалась!", "Результат теста", allure.attachment_type.TEXT)
        allure.attach(f"{rep.longrepr.reprcrash.message}", "Exception Message", allure.attachment_type.TEXT)
        allure.attach(f"{rep.longrepr.reprtraceback}", "Traceback", allure.attachment_type.TEXT)
