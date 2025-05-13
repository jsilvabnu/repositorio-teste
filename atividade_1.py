import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY_NOTICIAS")

if not api_key:
    raise ValueError("API Key não encontrada nas variáveis de ambiente")

url = "https://newsapi.org/v2/everything"

temas = []
quantidade_noticias = []

def menu():

    print("\nMENU")
    print("0. Sair")
    print("1. Consultar noticias")

    opcao = input("Digite a opção do menu: ")
    return opcao

def buscar_noticias():

    tema = input("Digite o tema que deseja pesquisar: ")
    temas.append(tema)
    headers = {
    'X-Api-Key': api_key
    }

    params = {
        'q': {tema},
        'language': "pt"
    }
    resposta = requests.get(url=url, headers=headers, params=params)
    print(resposta.status_code)

    resposta_json = resposta.json()


    for artigo in resposta_json["articles"][:quantidade]:
        print("\n")
        print("Título: ", artigo["title"])
        print("Descrição: ", artigo["description"])
        print("Fonte: ", artigo["url"])
        print("Autor: ", artigo["author"])

while True:

    opcao = menu()
    if opcao == "0":
        print("Saindo do sistema...")
        print("Você pesquisou sobre:", temas)
        print(f"Soma das notícias pesquisadas: {sum(quantidade_noticias)}.")
        
        break
    elif opcao == "1":
        try:
            quantidade = int(input("Digite a quantidade de noticia que deseja consultar (máximo de 5):"))
        except ValueError:
            print("Erro de valor. Tente novamente e digite um número válido.")
            continue

        if 5 >= quantidade > 0:
            quantidade_noticias.append(quantidade)
            buscar_noticias()

        else:
            print("Quantidade inválida. Tente novamente.")
    else:
        print("Opção inválida. Tente novamente.")


    
