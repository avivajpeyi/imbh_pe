RESULT_FILE = "(.*)injection(.*?)_result.json$"

H1L1_RESULT_FILE = "(.*)_H1L1_(.*)injection(.*?)_result.json$"
H1_RESULT_FILE = "(.*)_H1_(.*)injection(.*?)_result.json$"
L1_RESULT_FILE = "(.*)_L1_(.*)injection(.*?)_result.json$"
INJECTION_NUM = ".*injection(\\d+|$).*_result.json"

RESULT_FILE_GIVEN_I_NUMBER = (
    "(.*)_{detector_string}_(.*)injection{injection_number}_result.json$"
)
