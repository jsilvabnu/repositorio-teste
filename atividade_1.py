# Importa o módulo 'requests' para fazer requisições HTTP
import requests

# Importa o módulo 'os' para acessar variáveis de ambiente
import os

# Importa a função 'load_dotenv' do módulo 'dotenv' para carregar variáveis de ambiente de um arquivo .env
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env para o ambiente do sistema
load_dotenv()

# Recupera a chave da API para acessar as notícias a partir das variáveis de ambiente
api_key = os.getenv("API_KEY_NOTICIAS")

# Verifica se a chave da API foi encontrada nas variáveis de ambiente
# Se não, lança um erro com uma mensagem informando que a chave não foi encontrada
if not api_key:
    raise ValueError("API Key não encontrada nas variáveis de ambiente")

# Define a URL da API de notícias para realizar a consulta
url = "https://newsapi.org/v2/everything"

# Cria uma lista vazia chamada 'temas', que será usada para armazenar temas de pesquisa de notícias
temas = []

# Cria uma lista vazia chamada 'quantidade_noticias', que será usada para armazenar a quantidade de notícias a serem retornadas
quantidade_noticias = []

def menu():
    """
    Exibe um menú de opções para o usuário.

    - Solicita ao usuário que insira uma opção (0 ou 1).

    Saída:
    - Se usuário escolher opção 1, continua com a função buscar_noticias().
    - Se usuário escolher opção 0, retorna todos os temas pesquisados e a soma da quantidade de notícias pesquisadas.
    """

    print("\nMENU")
    print("0. Sair")
    print("1. Consultar noticias")

    opcao = input("Digite a opção do menu: ")
    return opcao

def buscar_noticias():
    """
    Usuário informa um tema da notícia, a função consulta notícias relacionadas via API NEWS e exibe os resultados solicitados.

    - Usuário informa um termo de pesquisa.
    - Adicina o tema da notícia a lista "temas".
    - Faz a requisição GET da API NEWS usando "API_KEY" e "URL".
    - Exibe o status da resposta.
    - Exibe o título, descrição, fonte e autor de cada notícia retornada.
    - Limita a 5 noticias.

    Requisitos:
    - Variáveis globais previamente definidas (tema, quantidade, API_KEY, url).
    - Importar a biblioteca requests.

    Saída:
    - Retorna ao usuário as informações das notícias encontradas de acordo com o tema solicitado.
    
    """

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

# Inicia um loop infinito para o menu, permitindo que o usuário interaja repetidamente
while True:

    # Chama a função 'menu()' que exibe as opções e recebe a escolha do usuário
    opcao = menu()

    # Se a opção escolhida for "0", sai do sistema
    if opcao == "0":
        print("Saindo do sistema...")

        # Exibe os temas que foram pesquisados durante a execução do programa
        print("Você pesquisou sobre:", ", ".join(temas))

        # Exibe a soma da quantidade de notícias pesquisadas até o momento
        print(f"Soma das notícias pesquisadas: {sum(quantidade_noticias)}.")
        
        # Interrompe o loop e finaliza o programa
        break

    # Se a opção escolhida for "1", permite ao usuário consultar notícias
    elif opcao == "1":
        try:
            # Solicita ao usuário a quantidade de notícias a serem consultadas (limite de 5)
            quantidade = int(input("Digite a quantidade de noticia que deseja consultar (máximo de 5):"))
        except ValueError:
            # Caso o usuário digite um valor inválido (não numérico), exibe um erro e continua o loop
            print("Erro de valor. Tente novamente e digite um número válido.")
            continue

        # Verifica se a quantidade digitada está entre 1 e 5
        if 5 >= quantidade > 0:
            # Adiciona a quantidade de notícias à lista 'quantidade_noticias'
            quantidade_noticias.append(quantidade)

            # Chama a função 'buscar_noticias()' para realizar a consulta de notícias
            buscar_noticias()

        else:
            # Caso a quantidade seja inválida (menor que 1 ou maior que 5), exibe uma mensagem de erro
            print("Quantidade inválida. Tente novamente.")

    # Caso o usuário digite uma opção inválida (diferente de 0 ou 1), exibe uma mensagem de erro
    else:
        print("Opção inválida. Tente novamente.")


    
