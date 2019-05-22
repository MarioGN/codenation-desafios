import requests
import json
import hashlib
from unittest import TestCase, main


token = '03407651289240a1205f9d478ac485d0810c3b7b'
url = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token='
url_post = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token='


def mount_url(url, token):
    return '{}{}'.format(url, token)

def make_request(api_url):
    response = requests.get(api_url)
    data = response.json()

    return data

def save_json(data):
    with open('answer.json', 'w') as f:
        json.dump(data, f)

def consultar_api():
    url_ = mount_url(url, token)
    data_ = make_request(url_)
    print(data_)
    save_json(data_)

def decifrar(mensagem, chave):
    mensagem = mensagem.lower()

    resultado = ''
    for l in mensagem:
        codigo = ord(l)

        if codigo > 96 and codigo < 123:
            codigo -= chave
            resultado += chr(codigo)
        else:
            resultado +=  l

    return resultado

def modify_json(file):
    with open(file, 'r') as jsonfile:
        data = json.load(jsonfile)

    mensagem = data['cifrado']
    chave = int(data['numero_casas'])

    decifrado = decifrar(mensagem, chave)

    data['decifrado'] = decifrado
    data['resumo_criptografico'] = hashlib.sha1(decifrado.encode()).hexdigest()
    
    with open(file, "w") as jsonFile:
        json.dump(data, jsonFile)

def send_response():
    url_ = mount_url(url_post, token)
    # headers = {'Content-type': 'multipart/form-data'}
    answer = {'answer': open('answer.json', 'rb')}

    r = requests.post(url_, files=answer)


class TestMakeRequest(TestCase):
    def test_make_request(self):
        url_ = mount_url(url, token)
        response = requests.get(url_)
        data = response.json()

        self.assertEqual(make_request(url_), data)


class TestMountUrl(TestCase):
    def test_mount_url(self):
        expected = '{}{}'.format(url, token)
        self.assertEqual(mount_url(url, token), expected)

    def test_mount_url_wrong(self):
        expected = '{}{}'.format(url, token)
        self.assertNotEqual(mount_url('https://www.google.com/', token), expected)


class TestDecifrar(TestCase):
    def test_decifrar_mensagem(self):
        expected = 'mario geroldi'
        msg = 'nbsjp hfspmej'

        self.assertEqual(decifrar(msg, 1), expected)


if __name__ == "__main__":
    consultar_api()
    modify_json('answer.json')
    send_response()
