
import pytest
import requests


def test_not_acceptable_http_method():
    response = requests.get("http://127.0.0.1:9292")
    assert response.status_code == 405


def test_not_acceptable_request():
    headers = {'accept': 'application/xml'}
    response = requests.post("http://127.0.0.1:9292", headers=headers)
    assert response.status_code == 406


def test_bad_request():

    headers = {'accept': 'application/json', 'content-type': 'application/xml'}
    response = requests.post("http://127.0.0.1:9292", headers=headers, json=dict(name="michelada",
                                                                                 email="hello@michelada.io"))
    assert response.status_code == 400


    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    response = requests.post("http://127.0.0.1:9292", headers=headers, json=dict())
    assert response.status_code == 400

    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    response = requests.post("http://127.0.0.1:9292", headers=headers)
    assert response.status_code == 400


def test_payload_incorrect():
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    response = requests.post("http://127.0.0.1:9292", headers=headers, json=dict(name="michelada",
                                                                                 emails="hello@michelada.io"))
    assert response.status_code == 422


def test_success():
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    response = requests.post("http://127.0.0.1:9292", headers=headers, json=dict(name="michelada",
                                                                                 email="hello@michelada.io"))
    assert response.status_code == 200

    headers = {'content-type': 'application/json'}
    response = requests.post("http://127.0.0.1:9292", headers=headers, json=dict(name="michelada",
                                                                                 email="hello@michelada.io"))
    assert response.status_code == 200


if __name__ == '__main__':
    test_success()
