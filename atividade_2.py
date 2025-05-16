import requests

import os

import time

from dotenv import load_dotenv

load_dotenv()

url = "https://jsonplaceholder.typicode.com/posts"

usuarios = []
posts_criados_localmente = []

quantidade_posts_visualizados = 0
quantidade_comentarios_visualizados = 0
quantidade_posts_criados = 0

def menu_inicial():
    """
    Exibe o menu principal do sistema e solicita a escolha do usuário.

    Opções disponíveis:
        0 - Sair do sistema
        1 - Fazer login
        2 - Cadastrar novo usuário

    Retorno:
        str: Opção escolhida pelo usuário (como string)
    """

    print("\nMenu de opções:")
    print("""
    0 - Sair
    1 - LOGIN
    2 - NOVO USUÁRIO
    """)
    return input("Escolha uma opção: ")

def menu_pos_login(codigo_usuario_logado):
    """
    Exibe o menu de opções para o usuário logado e executa ações com base na escolha.

    Parâmetros:
        codigo_usuario_logado (int): Identificador do usuário logado.

    Ações disponíveis:
        1 - Ver todos os posts
        2 - Ver todos os comentários
        3 - Ver apenas os posts do usuário logado
        4 - Ver posts de outro usuário
        5 - Criar novo post
        6 - Sair do menu

    """
    while True:
        print("\n=== MENU ===")
        print("1 - Ver posts")
        print("2 - Ver comentários")
        print("3 - Ver *meus* posts")
        print("4 - Ver posts de outro usuário")
        print("5 - Criar novo post") 
        print("6 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            ver_posts()
        elif escolha == "2":
            ver_comentarios()
        elif escolha == "3":
            ver_posts_do_usuario(codigo_usuario_logado)
        elif escolha == "4":
            ver_posts_de_outro_usuario()
        elif escolha == "5":
            criar_post(codigo_usuario_logado)  
        elif escolha == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def ver_posts():
    """
    Solicita uma quantidade ao usuário e exibe esse número de posts da API JSONPlaceholder.

    Funcionalidades:
        - Valida a entrada numérica
        - Faz requisição à API pública de posts
        - Exibe título e corpo dos posts
        - Atualiza contador global de visualizações

    Requisitos:
        - Variável global: quantidade_posts_visualizados
        - Bibliotecas: requests, time

    """

    try:
        quantidade = int(input("Quantos posts você deseja ver? "))
        if quantidade <= 0:
            print("Por favor, digite um número positivo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
        return

    resposta = requests.get("https://jsonplaceholder.typicode.com/posts")
    
    print("\nCarregando posts...")
    time.sleep(3)
    if resposta.status_code == 200:
        posts = resposta.json()
        global quantidade_posts_visualizados
        quantidade_posts_visualizados += quantidade
        for post in posts[:quantidade]:  # mostra apenas a quantidade escolhida
            
            print(f"\nID: {post['id']}")
            print(f"Título: {post['title']}")
            print(f"Corpo: {post['body']}")
    else:
        print("Erro ao carregar os posts.")

def ver_comentarios():
    """
    Solicita uma quantidade ao usuário e exibe esse número de comentários da API JSONPlaceholder.

    Funcionalidades:
        - Valida a entrada numérica
        - Faz requisição à API pública de comentários
        - Exibe e-mail e corpo do comentário
        - Atualiza contador global de visualizações

    Requisitos:
        - Variável global: quantidade_comentarios_visualizados
        - Bibliotecas: requests, time

    """
    try:
        quantidade = int(input("Quantos comentários você deseja ver? "))
        if quantidade <= 0:
            print("Por favor, digite um número positivo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
        return

    resposta = requests.get("https://jsonplaceholder.typicode.com/comments")
    
    print("\nCarregando comentários...")
    time.sleep(3)
    if resposta.status_code == 200:
        comentarios = resposta.json()
        global quantidade_comentarios_visualizados
        quantidade_comentarios_visualizados += quantidade
        for comentario in comentarios[:quantidade]:  # mostra apenas a quantidade escolhida
            
            print(f"\nID: {comentario['id']}")
            print(f"E-mail: {comentario['email']}")
            print(f"Comentário: {comentario['body']}")
    else:
        print("Erro ao carregar os comentários.")

def ver_posts_do_usuario(codigo_usuario_logado):
    """
    Exibe todos os posts feitos pelo usuário logado, tanto da API quanto os locais.

    Parâmetros:
        codigo_usuario_logado (int): ID do usuário logado

    Funcionalidades:
        - Busca posts da API com o userId do usuário
        - Verifica se há posts criados localmente por esse usuário
        - Exibe título e corpo de cada post encontrado

    Requisitos:
        - Lista global: posts_criados_localmente
        - Biblioteca: requests, time

    """
    print("\nCarregando posts do seu usuário...")
    time.sleep(2)

    resposta = requests.get("https://jsonplaceholder.typicode.com/posts")

    posts_usuario = []

    if resposta.status_code == 200:
        posts = resposta.json()

        for post in posts:
            if post["userId"] == codigo_usuario_logado:
                posts_usuario.append(post)
    else:
        print("Erro ao buscar posts da API.")

    # Verifica posts locais
    for post in posts_criados_localmente:
        if post["userId"] == codigo_usuario_logado:
            posts_usuario.append(post)

    # Exibe todos os posts encontrados
    if posts_usuario:
        for post in posts_usuario:
            print(f"\nUsuário: {post['userId']}")
            print(f"ID: {post['id']}")
            print(f"Título: {post['title']}")
            print(f"Corpo: {post['body']}")
    else:
        print("Este usuário não possui posts.")

def ver_posts_de_outro_usuario():
    """
    Solicita um ID de usuário e exibe todos os posts desse usuário a partir da API.

    Funcionalidades:
        - Valida entrada do ID
        - Busca na API todos os posts com esse userId
        - Exibe título e corpo dos posts encontrados

    Requisitos:
        - Biblioteca: requests, time

    """
    try:
        user_id = int(input("Digite o ID do usuário que você quer ver os posts: "))
        if user_id <= 0:
            print("Por favor, digite um número positivo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
        return

    print(f"\nCarregando posts do usuário {user_id}...")
    time.sleep(2)
    
    resposta = requests.get("https://jsonplaceholder.typicode.com/posts")

    if resposta.status_code == 200:
        posts = resposta.json()
        posts_usuario = []

        print(f"Segue abaixo posts do usuário {user_id}:")

        for post in posts:
            if post["userId"] == user_id:
                posts_usuario.append(post)

        if posts_usuario:
            for post in posts_usuario:
                print(f"\nID: {post['id']}")
                print(f"Título: {post['title']}")
                print(f"Corpo: {post['body']}")
        else:
            print("Este usuário não possui posts.")
    else:
        print("Erro ao buscar posts.")

def criar_post(codigo_usuario_logado):
    """
    Permite ao usuário logado criar um novo post e o envia para a API.

    Parâmetros:
        codigo_usuario_logado (int): ID do usuário que está criando o post

    Funcionalidades:
        - Recebe título e conteúdo do post
        - Envia dados via POST para a API
        - Salva o post em uma lista local
        - Atualiza o contador global de posts criados

    Requisitos:
        - Lista global: posts_criados_localmente
        - Variável global: quantidade_posts_criados
        - Bibliotecas: requests, time

    """
    print("\n=== Criar Novo Post ===")
    titulo = input("Digite o título do post: ")
    corpo = input("Digite o conteúdo do post: ")

    novo_post = {
        "userId": codigo_usuario_logado,
        "title": titulo,
        "body": corpo
    }

    print("\nEnviando post...")
    time.sleep(2)

    resposta = requests.post("https://jsonplaceholder.typicode.com/posts", json=novo_post)

    if resposta.status_code == 201:
        post_criado = resposta.json()
        print("Post criado com sucesso!")
        print(f"\nID: {post_criado['id']}")
        print(f"Título: {post_criado['title']}")
        print(f"Corpo: {post_criado['body']}")

        # Salva localmente
        posts_criados_localmente.append(post_criado)
        global quantidade_posts_criados
        quantidade_posts_criados += 1
    else:
        print("Erro ao criar o post.")

def cadastrar_usuario(usuarios):
    """
    Cadastra um novo usuário e o adiciona na lista de usuários existentes.

    Parâmetros:
        usuarios (list): Lista onde os dados dos usuários são armazenados

    Ações:
        - Solicita email e senha
        - Atribui um novo código automático
        - Adiciona o usuário à lista

    """
    usuario = {}
    usuario["codigo"] = len(usuarios)+1
    usuario["email"] = input("Digite o email: ")
    usuario["senha"] = input("Digite a senha: ")
    usuarios.append(usuario)
    print("Usuário cadastrado com sucesso!")
    print(usuarios)

def login():
    """
    Realiza o login do usuário verificando e-mail e senha.

    Ações:
        - Solicita credenciais do usuário
        - Verifica se e-mail e senha correspondem a um usuário cadastrado
        - Em caso de sucesso, chama o menu pós-login
        - Exibe mensagem de erro caso as credenciais estejam incorretas

    Requisitos:
        - Lista global: usuarios
    """
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")

    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            print("Login realizado com sucesso!")
            print(f"Bem-vindo, usuário de código {usuario['codigo']}")
            menu_pos_login(usuario["codigo"])
            return
    print("Email ou senha incorretos. Tente novamente.")

while True:
    opcao = menu_inicial()
   
    if opcao == "0":
        print("\n=== Resumo da Sessão ===")
        print(f"Total de posts visualizados: {quantidade_posts_visualizados}")
        print(f"Total de comentários visualizados: {quantidade_comentarios_visualizados}")
        print(f"Total de posts criados: {quantidade_posts_criados}")
        print("Saindo do programa.")
        break
    elif opcao == "1":
        login()
    elif opcao == "2":
        cadastrar_usuario(usuarios)
    else:
        print("Opção inválida.")
