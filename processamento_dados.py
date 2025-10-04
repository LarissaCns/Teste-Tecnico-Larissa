"""Processamento de Dados: Extração, Transformação e Geração de SQL."""
import zipfile
import pandas as pd

DADOS = "dados.zip"
EXTRAIR_PARA = "."

def descompactar_arquivos(zip_path, extrair_para):
    """Extrai um arquivo zip para o diretório especificado.

    Args:
        zip_path (str): Caminho do arquivo zip a ser descompactado.
        extrair_para (str): Diretório onde os arquivos serão extraídos.
    Raises:
        Exception: Se ocorrer algum erro durante a descompactação.
    """
    print(f"Descompactando {zip_path} para {extrair_para} ...")
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extrair_para)
        print(f"O arquivo {zip_path} foi extraído para {extrair_para} com sucesso. \n")
    except Exception as e:
        print(f"Erro durante a descompactação: {e}")
        raise


def carregar_dados(caminho_arquivo):
    """Carrega dados de um arquivo CSV para um DataFrame do pandas.
    Args:
        caminho_arquivo (str): Caminho do arquivo CSV.
    Returns:
        pd.DataFrame: DataFrame contendo os dados carregados.
    Raises:
        Exception: Se ocorrer algum erro durante o carregamento dos dados.
    """
    try:
        df = pd.read_csv(caminho_arquivo)
        print(f"Dados carregados com sucesso de {caminho_arquivo}. \n")
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        raise


def filtrar_dados(df, coluna, valor):
    """Filtra o DataFrame com base em uma condição na coluna especificada.
    Args:
        df (pd.DataFrame): DataFrame a ser filtrado.
        coluna (str): Nome da coluna para aplicar o filtro.
        valor: Valor que a coluna deve ter para incluir a linha no resultado.
    Returns:
        pd.DataFrame: DataFrame filtrado.
    Raises:
        Exception: Se ocorrer algum erro durante o filtro.
    """
    try:
        df_filtrado = df[df[coluna] == valor].copy()
        print(f"Dados filtrados onde {coluna} == {valor}. \n")
        return df_filtrado
    except Exception as e:
        print(f"Erro ao filtrar dados: {e}")
        raise


def ordenar_por_data(df, coluna_data):
    """Ordena o DataFrame pela coluna de data/hora especificada.
    Args:
        df (pd.DataFrame): DataFrame a ser ordenado.
        coluna_data (str): Nome da coluna de data/hora.
    Returns:
        pd.DataFrame: DataFrame ordenado.
    Raises:
        Exception: Se ocorrer algum erro durante a ordenação.
    """
    try:
        df[coluna_data] = pd.to_datetime(df[coluna_data])
        df_ordenado = df.sort_values(by=coluna_data)
        print(f"Dados ordenados por {coluna_data}. \n")
        return df_ordenado
    except Exception as e:
        print(f"Erro ao ordenar dados: {e}")
        raise


def juntar_dados_com_tipos(df_dados, df_tipos):
    """Junta o DataFrame de dados com o de tipos para adicionar o nome do tipo.
    Args:
        df_dados (pd.DataFrame): DataFrame contendo os dados principais.
        df_tipos (pd.DataFrame): DataFrame contendo os tipos.
    Returns:
        pd.DataFrame: DataFrame resultante da junção.
    Raises:
        Exception: Se ocorrer algum erro durante a junção.
    """
    try:
        df_tipos_renomeado = df_tipos.rename(
            columns={"id": "tipo_id", "nome": "nome_tipo"}
        )
        df_dados_renomeado = df_dados.rename(columns={"tipo": "tipo_id"})
        df_final = pd.merge(
            df_dados_renomeado, df_tipos_renomeado, on="tipo_id", how="left"
        )
        print("Dados juntados com os tipos com sucesso. \n")
        return df_final
    except Exception as e:
        print(f"Erro ao juntar os dataframes: {e}")
        raise


def gerar_sql_inserts(df, nome_tabela, nome_arquivo):
    """
    Gera um arquivo .sql com comandos INSERT a partir de um DataFrame,
    construindo a query de forma dinâmica a partir de uma lista de colunas.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem inseridos.
        nome_tabela (str): Nome da tabela onde os dados serão inseridos.
        nome_arquivo (str): Nome do arquivo .sql a ser gerado.
    Raises:
        Exception: Se ocorrer algum erro durante a geração do arquivo SQL.
    """
    print(f"Gerando arquivo de inserts '{nome_arquivo}'...")
    try:
        colunas_para_insert = ["created_at", "status", "tipo_id", "nome_tipo"]

        colunas_sql = ", ".join(colunas_para_insert)

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo_sql:
            for _, row in df.iterrows():
                valores = []
                for coluna in colunas_para_insert:
                    valor = row[coluna]

                    if pd.api.types.is_number(valor):
                        valores.append(str(valor))
                    else:
                        valor_escapado = str(valor).replace("'", "''")
                        valores.append(f"'{valor_escapado}'")

                valores_sql = ", ".join(valores)

                query = f"INSERT INTO {nome_tabela} ({colunas_sql}) VALUES ({valores_sql});\n"

                arquivo_sql.write(query)

        print(f"Arquivo '{nome_arquivo}' gerado com sucesso. \n")

    except KeyError as e:
        print(
            f"Erro: A coluna {e} não foi encontrada no DataFrame."
            f"Verifique a lista 'colunas_para_insert'."
        )
        raise
    except Exception as e:
        print(f"Erro ao gerar o arquivo SQL: {e}")
        raise


if __name__ == "__main__":
    print("Processamento de Dados Iniciado")
    print("-------------------------------- \n")
    descompactar_arquivos(DADOS, EXTRAIR_PARA)

    print("\n Carregando dados...")
    origem_dados = carregar_dados("origem-dados.csv")
    print(origem_dados.head())

    print("\n Filtrando dados...")
    dados_filtrados = filtrar_dados(origem_dados, "status", "CRITICO")
    print(dados_filtrados.head())

    print("\n Ordenando dados por data/hora...")
    dados_ordenados = ordenar_por_data(dados_filtrados, "created_at")
    print(dados_ordenados.head())

    print("\n Filtrando tipos específicos...")
    tipos = carregar_dados("tipos.csv")
    print(tipos.head())

    print("\n Juntando dados com tipos...")
    dados_com_tipos = juntar_dados_com_tipos(dados_ordenados, tipos)
    print(dados_com_tipos.head())

    print("\n Gerando arquivo SQL...")
    gerar_sql_inserts(
        df=dados_com_tipos, nome_tabela="dados_finais", nome_arquivo="insert-dados.sql"
    )

    print("\n Adicionando query de agregação ao arquivo SQL...")
    QUERY_AGREGACAO = """
    -- Query para retornar, por dia, a quantidade de itens agrupadas pelo tipo.
    SELECT
        CAST(created_at AS DATE) AS dia,
        nome_tipo,
        COUNT(id) AS quantidade
    FROM
        dados_finais
    GROUP BY
        dia,
        nome_tipo
    ORDER BY
        dia,
        nome_tipo;
    """

    with open("insert-dados.sql", "a", encoding="utf-8") as f:
        f.write("\n\n" + QUERY_AGREGACAO)

    print("\nProcessamento de Dados Finalizado!")
