import pytest

from consts import Filenames, Scopes, Test_Data_Keys as Keys
from utils import json_utils, random_utils

# Файл с тестовыми данными
test_file = Filenames.TEST_FILE_DIRECT_CODING
test_data = json_utils.json_to_dict(test_file)

endpoint = test_data[Keys.URL]

# Списки данных для разных тест-кейсов
valid_cases = test_data[Keys.VALID_CASES]
invalid_fields_cases = test_data[Keys.INVALID_FIELDS_CASES]
too_large_params_cases = test_data[Keys.TOO_LARGE_PARAMS_CASES]

# Динамические ID для разных тест-кейсов на основе используемых данных
id_list_valid = list(map(lambda c: "запрос = {}".format(c[Keys.REQ_PARAMS][Keys.Q]
                                                        if Keys.Q in c[Keys.REQ_PARAMS]
                                                        else c[Keys.REQ_PARAMS][Keys.STREET]), valid_cases))
id_list_invalid_fields = list(
    map(lambda c: " ".join(["{}={}".format(k, v) for k, v in c[Keys.REQ_PARAMS].items()]), invalid_fields_cases))
id_list_too_large_params = list(
    map(lambda c: " ".join(["{}={}".format(k, v) for k, v in c[Keys.REQ_PARAMS].items()]), too_large_params_cases))


# Фикстуры для позитивных тест кейсов с валидными данными
@pytest.fixture(scope=Scopes.CLASS, params=valid_cases, ids=id_list_valid)
def test_data_valid(request):
    return request.param


@pytest.fixture(scope=Scopes.CLASS, name="valid_response")
def direct_geocoding_valid_req(test_data_valid, request_get):
    return request_get(url=endpoint, params=test_data_valid[Keys.REQ_PARAMS])


@pytest.fixture(scope=Scopes.CLASS, name="valid_expected")
def direct_geocoding_get_valid_expected(test_data_valid):
    return test_data_valid[Keys.EXPECTED]


# Фикстуры для негативных тест кейсов с невалидными обязательными параметрами (широта и долгота)
@pytest.fixture(scope=Scopes.CLASS, params=invalid_fields_cases, ids=id_list_invalid_fields)
def test_data_invalid_fields(request):
    return request.param


@pytest.fixture(scope=Scopes.CLASS, name="invalid_fields_response")
def reverse_geocoding_invalid_fields_req(test_data_invalid_fields, request_get):
    return request_get(url=endpoint, params=test_data_invalid_fields[Keys.REQ_PARAMS])


@pytest.fixture(scope=Scopes.CLASS, name="invalid_fields_expected")
def reverse_geocoding_get_invalid_fields_expected(test_data_invalid_fields):
    return test_data_invalid_fields[Keys.EXPECTED]


# Фикстуры для негативных тест кейсов с длиной параметров, превышающей допустимую
@pytest.fixture(scope=Scopes.CLASS, params=too_large_params_cases, ids=id_list_too_large_params)
def test_data_too_large_params(request):
    return request.param


@pytest.fixture(scope=Scopes.CLASS, name="too_large_params_response")
def reverse_geocoding_too_large_params_req(too_large_params_response, test_data_too_large_params):
    return too_large_params_response(endpoint, test_data_too_large_params)


@pytest.fixture(scope=Scopes.CLASS, name="too_large_params_expected")
def direct_geocoding_get_too_large_params_expected(test_data_too_large_params):
    return test_data_too_large_params[Keys.EXPECTED]
