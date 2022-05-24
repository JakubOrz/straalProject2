import json
import requests


def test_connection():
    assert requests.get("http://127.0.0.1:3000/").status_code != 404


def test_report_1():
    with open("test_data/report_test1_request_body.json") as json_file:
        request_body = json.load(json_file)
        result = requests.post(
            "http://127.0.0.1:3000/report",
            json=request_body,
            headers={'content-type': 'application/json'}
        )
        assert result.status_code == 200
    with open("test_data/report_test1_expected_response.json") as expected_response_file:
        expected_response = json.load(expected_response_file)

    for expected_payment, response_payment in zip(expected_response, result.json()):
        assert expected_payment['description'] == response_payment['description']
        assert expected_payment['date'] == response_payment['date']
        assert expected_payment['currency'] == response_payment['currency']
        assert expected_payment['amount'] == response_payment['amount']
        assert expected_payment['payment_mean'] == response_payment['payment_mean']
