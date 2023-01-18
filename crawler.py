from bs4 import BeautifulSoup
import requests
from sqlalchemy.orm import Session
from app import database, models
import re

url = "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf"


def main():

    reset_db = True
    if reset_db:
        database.drop_db()
        database.create_db()

    else:
        database.create_db()

    session = database.SessionLocal()
    parse_oferta(508, 2022, 2, session)


def parse_oferta(dep_id, ano, periodo, session: Session):
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

    response = requests.request("POST", url, headers=headers, data=payload)
    html_soup = BeautifulSoup(response.text.encode('utf8'), 'html.parser')

    # para cada disciplina encontrada
    disciplinas_professores = html_soup.find_all('tbody')[1].find_all('tr')
    len_disciplinas = len(html_soup.find_all('tbody')[1].find_all(class_='agrupador'))
    indice_disciplina_atual = 0

    disciplina = None

    for i, disciplina_professor in enumerate(disciplinas_professores):

        type = disciplinas_professores[i].attrs['class'][0]
        if type == 'agrupador':


            indice_disciplina_atual += 1
            print(f'Parsing disciplina {indice_disciplina_atual}/{len_disciplinas}')
            codigo_e_disciplina = disciplina_professor.td.a.span.text.split(' - ')
            disciplina = models.Disciplina(codigo=codigo_e_disciplina[0], nome=codigo_e_disciplina[1])
            continue

        elif type == 'linhaPar' or type == 'linhaImpar':
            nome_professor = re.match(r'(\w* )*', disciplina_professor.find(name='td', class_='nome').text).group(
                0).rstrip()
            # existe_professor = professor
            professor = session.query(models.Professor).filter(models.Professor.nome == nome_professor).first()
            if not professor:
                professor = models.Professor(nome=nome_professor)
                session.add(professor)

            if professor not in disciplina.professores:
                disciplina.professores.append(professor)
            session.commit()

            print("Professor encontrado")
            continue
        else:
            print("Não é professor nem disciplina")
    session.close()


def get_request_from_oferta():
    response = requests.request("GET", url)
    html_soup = BeautifulSoup(response.text.encode('utf8'), 'html.parser')
    return {"cookies": response.headers["Set-Cookie"].split(' ')[0],
            "javax": html_soup.select('#javax\.faces\.ViewState')[0]['value']}


if __name__ == '__main__':
    main()
