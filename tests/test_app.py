from http import HTTPStatus


def test_ping_deve_retornar_ok_e_pong(client):
    response = client.get('/ping')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'pong'}
