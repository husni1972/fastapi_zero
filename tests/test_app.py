from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_ola_mundo():
    client = TestClient(app)  # Arrange

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_read_aula02():
    client = TestClient(app)  # Arrange

    response = client.get('/aula02')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert '<h1> Olá Mundo! </h1>' in response.text  # Assert
