from http import HTTPStatus

from fastapi_zero.schemas import UserPublic
from fastapi_zero.security import create_access_token


def test_get_current(client, token, user_ficticio):
    response = client.get(
        '/users/current',
        headers={'Authorization': f'Bearer {token}'},
    )  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
         'username': user_ficticio.username,
         'email': user_ficticio.email,
         'id': user_ficticio.id,
    }


def test_create_user(client):
    # response = client.get('/users/')  # Act

    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'teste@teste.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.CREATED  # Assert
    assert response.json() == {
        'username': 'Teste',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_create_user_exist_user(client, user_ficticio):
    response = client.post(  # Act
        '/users/',
        json={
            'username': user_ficticio.username,
            'email': 'teste2@teste.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT  # Assert
    assert response.json() == {'detail': 'User already exists'}


def test_create_user_exist_email(client, user_ficticio):
    response = client.post(  # Act
        '/users/',
        json={
            'username': 'Teste2',
            'email': user_ficticio.email,
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT  # Assert
    assert response.json() == {'detail': 'Email already exists'}


def test_get_user_without_email(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_user_without_user(client):
    data = {'sub': 'teste@teste.com'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_without_users(client):
    response = client.get('/users/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'users': []}


def test_read_with_users(client, user_ficticio):
    user_schema = UserPublic.model_validate(user_ficticio).model_dump()
    response = client.get('/users/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user_ficticio):
    user_schema = UserPublic.model_validate(user_ficticio).model_dump()
    response = client.get(f'/users/{user_ficticio.id}')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == user_schema


def test_read_user_not_found(client):
    response = client.get('/users/2')  # Act

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user_ficticio, token):
    response = client.put(
        f'/users/{user_ficticio.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'testtest',
        },
    )  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user_ficticio.id,
    }


def test_delete_user(client, user_ficticio, token):
    response = client.delete(
        f'/users/{user_ficticio.id}',
        headers={'Authorization': f'Bearer {token}'},
    )  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'User deleted'}


# Deixa de ter o teste abaixo pois um usuário não pode atualizar algo diferente
# das próprias informações
# def test_update_user_not_found(client):
#     response = client.put(
#         '/users/2',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'bob',
#             'email': 'bob@example.com',
#             'password': 'testtest',
#         },
#     )  # Act

#     assert response.status_code == HTTPStatus.NOT_FOUND  # Assert
#     assert response.json() == {'detail': 'User not found'}


# PERDE O SENTIDO POIS NÃO ESTA SE BUSCANDO MAIS BUSCANDO A
# INFORMAÇÃO DO BANCO DE DADOS
# def test_update_user_integrityerror(
#     client, user_ficticio, user_ficticio2, token
# ):
#     response = client.put(
#         f'/users/{user_ficticio.id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'Teste2',
#             'email': 'bob@example.com',
#             'password': 'testtest',
#         },
#     )  # Act

#     assert response.status_code == HTTPStatus.CONFLICT  # Assert
#     assert response.json() == {'detail': 'Username or Email already exists'}


# Deixa de ter o teste abaixo pois um usuário não pode deletar algo diferente
# das próprias informações
# def test_delete_user_not_found(client, token):
#     response = client.delete(
#         '/users/2',
#         headers={'Authorization': f'Bearer {token}'},
#     )  # Act
#     assert response.status_code == HTTPStatus.NOT_FOUND  # Assert
#     assert response.json() == {'detail': 'User not found'}


# def test_read_aula02(client):
#     response = client.get('/aula02')  # Act

#     assert response.status_code == HTTPStatus.OK  # Assert
#     assert '<h1> Olá Mundo! </h1>' in response.text  # Assert
