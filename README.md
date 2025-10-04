# Projeto de Teste Técnico: Pipeline de Dados e API RESTful

Este projeto foi desenvolvido como parte de um processo seletivo e consiste em duas partes principais:

1.  Um **script de pipeline de dados** (`processamento_dados.py`) que realiza um processo de ETL (Extração, Transformação e Carga): extrai dados de arquivos CSV, os transforma utilizando a biblioteca Pandas e gera um arquivo `.sql` com os comandos de inserção para um banco de dados.
2.  Uma **API RESTful** (`api.py`) desenvolvida com Flask que expõe um endpoint para consultar informações do arquivo `tipos.csv`.

## 🚀 Funcionalidades

### Parte 1: Script de Processamento de Dados
- **Descompactação:** Extrai automaticamente os arquivos de um `dados.zip`.
- **Leitura e Processamento:** Carrega os dados dos arquivos `origem-dados.csv` e `tipos.csv` em DataFrames do Pandas.
- **Transformação:**
    - Filtra os dados para manter apenas os registros com status "CRÍTICO".
    - Ordena os resultados pela data de criação (`created_at`).
    - Enriquece os dados, adicionando o nome do tipo (`nome_tipo`) através do cruzamento com as informações do arquivo de tipos.
- **Geração de Saída:** Gera um arquivo `insert-dados.sql` contendo todos os comandos `INSERT` formatados para popular uma tabela `dados_finais`.

### Parte 2: API RESTful
- **Servidor Web:** Utiliza Flask para criar um servidor web local.
- **Leitura Eficiente:** Carrega os dados do `tipos.csv` em um dicionário na memória no momento da inicialização para garantir consultas rápidas.
- **Endpoint de Consulta:** Expõe o endpoint `GET /tipo/<id>` para consultar o nome de um tipo com base no seu ID.
- **Respostas em JSON:** Retorna os dados no formato JSON, o padrão para APIs web.
- **Tratamento de Erros:** Retorna uma mensagem de erro e o status HTTP 404 caso um ID não seja encontrado.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Pandas:** Para manipulação e análise de dados no script principal.
- **Flask:** Para o desenvolvimento da API RESTful.
- **Módulo `csv`:** (Nativo do Python) Para a leitura de dados na API.

## 📋 Pré-requisitos

Antes de começar, você vai precisar ter o [Python 3](https://www.python.org/) instalado em sua máquina.

## ⚙️ Instalação e Configuração

Siga os passos abaixo para configurar o ambiente e executar o projeto:

1.  **Clone este repositório ou baixe os arquivos do projeto.**

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd NOME-DA-SUA-PASTA
    ```

3.  **Crie um ambiente virtual:**
    ```bash
    python -m venv venv
    ```

4.  **Ative o ambiente virtual:**
    - **No Windows:**
        ```bash
        venv\Scripts\activate
        ```
    - **No macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```

5.  **Instale as dependências do projeto:**
    ```bash
    pip install -r requirements.txt
    ```
