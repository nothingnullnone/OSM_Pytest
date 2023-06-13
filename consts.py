import pathlib


class Filenames:
    TEST_FILE_DIRECT_CODING = str(pathlib.Path(__file__).parent.resolve()) + "\\resources\\test_data_direct.json"
    TEST_FILE_REVERSE_CODING = str(
        pathlib.Path(__file__).parent.resolve()) + "\\resources\\test_data_reverse.json"
    SCHEMA_DIRECT_CODING = str(pathlib.Path(__file__).parent.resolve()) + "\\resources\\json_schemas" \
                                                                          "\\direct_geocoding_response_schema.json"
    SCHEMA_REVERSE_CODING = str(pathlib.Path(__file__).parent.resolve()) + "\\resources\\json_schemas" \
                                                                           "\\reverse_geocoding_response_schema.json"
    SCHEMA_CODING_ERROR = str(
        pathlib.Path(__file__).parent.resolve()) + "\\resources\\json_schemas\\geocoding_error_schema.json"
    LOGS_FILE = str(pathlib.Path(__file__).parent.resolve()) + "\\logs\\logs.log"


class Encodings:
    UTF8 = "utf8"
    UTF16 = "utf16"
    ASCII = "ascii"
    CP1251 = "cp1251"


class Scopes:
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
    PACKAGE = "package"
    SESSION = "session"


class Test_Data_Keys:
    ADDRESS = "address"
    CITY = "city"
    CODE = "code"
    COUNTRY = "country"
    DISPLAY_NAME = "display_name"
    ERROR = "error"
    EXPECTED = "expected"
    INVALID_FIELDS_CASES = "invalid_fields_cases"
    LAT = "lat"
    LEN = "len"
    LON = "lon"
    MESSAGE = "message"
    NO_REQUIRED_FIELDS_CASES = "no_required_fields_cases"
    Q = "q"
    REL_TOL = "rel_tol"
    REQ_PARAMS = "req_params"
    STREET = "street"
    TOO_LARGE_PARAMS_CASES = "too_large_params_cases"
    URL = "url"
    VALID_CASES = "valid_cases"
