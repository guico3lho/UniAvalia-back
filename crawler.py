from bs4 import BeautifulSoup
import requests

url = "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf"
import models
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import database
import re


def main():
    reset_db = True
    if reset_db:
        database.drop_db()
        database.create_db()

    else:
        database.create_db()

    session = database.SessionLocal()
    parse_oferta(508, 2022, 2, session)
    # send_sqlalchemy_sqlite(disciplinas_list, session)


# Para cada matéria, criar objeto do tipo disciplina
# para cada professor da matéria, criar objeto do tipo professor
# conectar disciplina com professor

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
    disciplinas_list = []
    response = requests.request("POST", url, headers=headers, data=payload)
    html_soup = BeautifulSoup(response.text.encode('utf8'), 'html.parser')

    # para cada disciplina encontrada
    disciplinas_professores = html_soup.find_all('tbody')[1].find_all('tr')
    len_disciplinas = len(html_soup.find_all('tbody')[1].find_all(class_='agrupador'))
    indice_disciplina_atual = 0

    disciplina = None
    professor = None
    flag_nova_disciplina_encontrada = 0
    for i, disciplina_professor in enumerate(disciplinas_professores):

        type = disciplinas_professores[i].attrs['class'][0]
        if type == 'agrupador':
            # if flag_nova_disciplina_encontrada == 1:
            #     session.add(disciplina)
            #     session.commit()

            flag_nova_disciplina_encontrada = 1
            indice_disciplina_atual += 1
            print(f'Parsing disciplina {indice_disciplina_atual}/{len_disciplinas}')
            codigo_e_disciplina = disciplina_professor.td.a.span.text.split(' - ')
            # disciplina = {'codigo': codigo_e_disciplina[0], 'nome': codigo_e_disciplina[1]}
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

#
# SELECT d.nome, p.nome
# FROM disciplina_professor dp
# INNER JOIN disciplina d ON d.id = dp.disciplina_id
# INNER JOIN professor p ON p.id = dp.professor_id



def get_request_from_oferta():
    response = requests.request("GET", url)
    html_soup = BeautifulSoup(response.text.encode('utf8'), 'html.parser')
    return {"cookies": response.headers["Set-Cookie"].split(' ')[0],
            "javax": html_soup.select('#javax\.faces\.ViewState')[0]['value']}
    # disciplinas_span = html_soup.find_all('span', class_='tituloDisciplina')
    # for disciplina_parent in disciplinas_span:
    #     codigo_disciplina = disciplina_parent.text
    #     codigo, nome = codigo_disciplina.split(' - ')
    #     disciplinas_list.append({'codigo': codigo, 'nome': nome})
    #
    # return disciplinas_list

    # url_api = 'http://127.0.0.1:8000/disciplinas/'
    # response = requests.post(url_api, json=disciplinas_list)
    # if response.status_code == 200:
    #     print(response.json())
    # else:
    #     print(response.status_code)





# def send_sqlalchemy_sqlite(disciplinas_list, s: Session):
#     data = [models.Disciplina(**d) for d in disciplinas_list]
#     s.add_all(data)
#     s.commit()


if __name__ == '__main__':
    main()
