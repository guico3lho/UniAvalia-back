from bs4 import BeautifulSoup
import requests
url = "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf"


def main():
    parse_oferta(508, 2022,2)


def parse_oferta(dep_id, ano,periodo):
    request_data = get_request_from_oferta()
    payload = f'formTurma=formTurma&formTurma%3AinputNivel=G&formTurma%3AinputDepto={dep_id}&formTurma%3AinputAno={ano}&formTurma%3AinputPeriodo={periodo}&formTurma%3Aj_id_jsp_1370969402_11=Buscar&javax.faces.ViewState=' \
              f'{request_data["javax"]}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': url,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://sigaa.unb.br',
        'Connection': 'keep-alive',
        'Cookie': request_data['cookies'],
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    disciplinas_list = []
    response = requests.request("POST", url, headers=headers, data=payload)
    html_soup = BeautifulSoup(response.text.encode('utf8'), 'html.parser')

    disciplinas_span = html_soup.find_all('span', class_='tituloDisciplina')
    for disciplina_parent in disciplinas_span:
        codigo_disciplina = disciplina_parent.text
        codigo, nome = codigo_disciplina.split(' - ')
        disciplinas_list.append({'codigo': codigo, 'nome': nome})

    return disciplinas_list
    # url_api = 'http://127.0.0.1:8000/disciplinas/'
    # response = requests.post(url_api, json=disciplinas_list)
    # if response.status_code == 200:
    #     print(response.json())
    # else:
    #     print(response.status_code)


def get_request_from_oferta():
    response = requests.request("GET", url)
    html_soup = BeautifulSoup(response.text.encode('utf8'), 'html.parser')
    return {"cookies": response.headers["Set-Cookie"].split(' ')[0],
            "javax": html_soup.select('#javax\.faces\.ViewState')[0]['value']}

if __name__ == '__main__':
    main()