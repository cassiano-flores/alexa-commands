import requests
import base64
import os
from datetime import datetime, timedelta, timezone

# Configurações do repositório e do token do GitHub
GITHUB_TOKEN = "your_key_here"  #os.getenv('GITHUB_TOKEN')
REPO_OWNER = "cassiano-flores"  # Seu nome de usuário do GitHub
REPO_NAME = "alexa-commands"  # Nome do repositório

def get_commit_message():
    # Definir o fuso horário de GMT-3
    gmt_minus_3 = timezone(timedelta(hours=-3))

    # Obter a data e hora atuais
    timestamp = datetime.now(gmt_minus_3).strftime("%Y-%m-%d %H:%M:%S")

    return f"commit day {timestamp}"

def commit_to_github():
    # Caminho do arquivo no repositório
    file_path = "README.md"  # Altere isso para o arquivo que deseja modificar
    branch = "main"  # Altere para a branch correta

    # URL da API do GitHub para obter o conteúdo do arquivo
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"

    # Cabeçalhos de autenticação
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. Obter o conteúdo atual do arquivo para pegar o SHA
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erro ao obter o arquivo: {response.content.decode()}")

    file_data = response.json()
    sha = file_data['sha']
    content = base64.b64decode(file_data['content']).decode()

    # 2. Gerar a mensagem de commit com o timestamp
    commit_message = get_commit_message()

    # 3. Modificar o conteúdo, adicionando o commit_message no final
    new_content = content + f"\n{commit_message}"

    # 4. Codificar o novo conteúdo em Base64
    encoded_content = base64.b64encode(new_content.encode()).decode()

    # 5. Preparar os dados para o commit
    commit_data = {
        "message": commit_message,
        "content": encoded_content,
        "sha": sha,
        "branch": branch
    }

    # 6. Enviar o commit via API
    commit_response = requests.put(url, headers=headers, json=commit_data)
    if commit_response.status_code != 200:
        raise Exception(f"Erro ao commitar no GitHub: {commit_response.content.decode()}")
