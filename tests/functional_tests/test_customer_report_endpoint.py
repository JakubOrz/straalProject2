import json
import string
import random

import requests


def test_customer_report_1():
    with open("test_data/client_report_test_1_request_body.json") as json_file:
        request_body = json.load(json_file)
        result = requests.post(
            "http://127.0.0.1:3000/customer-report",
            json=request_body,
            headers={'content-type': 'application/json'}
        )
    assert result.status_code == 200
    with open("test_data/client_report_test_1_expected_response.json") as expected_response_file:
        expected_response = json.load(expected_response_file)

    assert expected_response == result.json()


def test_get_no_existing_customer_report():
    # No real customer has 5 digit id, so there is no way it will exist in service
    random_customer_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    result = requests.get(
        url=f"http://127.0.0.1:3000/customer-report/{random_customer_id}"
    )
    assert result.status_code == 404


def test_get_customer_report():
    with open("test_data/client_report_test_1_request_body.json") as json_file:
        customer_id = json.load(json_file)['customer_id']
    result = requests.get(
        url=f"http://127.0.0.1:3000/customer-report/{customer_id}"
    )
    assert result.status_code == 200

    with open("test_data/client_report_test_1_expected_response.json") as expected_response_file:
        expected_response = json.load(expected_response_file)
    assert result.json() == expected_response, \
        "Loaded report should be the same as generated in 'test_customer_report_1'"
