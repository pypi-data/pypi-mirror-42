import requests
import json


def ResponseGet(token=None, url=None):
    headers = {'content-type': 'application/json', 'Accept': 'application/json'}
    if token:
        headers.update({'AuthToken': token})
    response = requests.get(url, headers=headers)
    response_dict = json.loads(response.text)
    return response_dict


def ResponsePost(token, url, data={}):
    data = json.dumps(data)
    headers = {'AuthToken': token, 'content-type': 'application/json', 'Accept': 'application/json'}
    responose = requests.post(url, data=data, headers=headers)
    responose_dict = json.loads(responose.text)
    return responose_dict


def GetToken(login, password):
    data = {'Login': login, 'Senha': password}
    token_url = "https://api.fidelimax.com.br/api/Integracao/GetToken"
    responose = requests.post(token_url, data=data)
    if responose.status_code == 200:
        responose_dict = json.loads(responose.text)
        if responose_dict.get('CodigoResposta') == 100:
            return responose_dict.get('token')
        else:
            return responose_dict


def LojaPertencentesPrograma(login, password):
    token = GetToken(login, password)
    url = "https://api.fidelimax.com.br/api/Integracao/LojaPertencentesPrograma?token={'%s'}" % token
    return ResponseGet(token, url)


def CadastrarConsumidor(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/CadastrarConsumidor"
    token = GetToken(login, password)
    # data['token_externo'] = token
    # data['nome'] = 'Yogesh'
    # data['cpf'] ='123'
    # data['sexo'] ='Masculinao'
    # data['nascimento'] = '12/08/1990'
    # data['email'] = 'yogesh@tkobr.com'
    # data['telefone'] = '(51)99999-9999'
    # data['saldo'] = 1

    return ResponsePost(token, url, data)


def AtualizarConsumidor(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/AtualizarConsumidor"
    token = GetToken(login, password)
    return ResponsePost(token, url, data)


def ConsultaConsumidor(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/ConsultaConsumidor"
    token = GetToken(login, password)
    return ResponsePost(token, url, data)


def RetornaDadosCliente(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/RetornaDadosCliente"
    token = GetToken(login, password)
    return ResponsePost(token, url, data)


def ResgataPremio(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/ResgataPremio"
    token = GetToken(login, password)
    return ResponsePost(token, url, data)


def PontuaConsumidor(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/PontuaConsumidor"
    token = GetToken(login, password)
    return ResponsePost(token, url, data)


def ListaProdutos(login, password):
    url = "https://api.fidelimax.com.br/api/Integracao/ListaProdutos"
    token = GetToken(login, password)
    return ResponseGet(token, url)
