"""API Flask para consulta de tipos por ID."""
import csv
from flask import Flask, jsonify


app = Flask(__name__)

tipos_map = {}
try:
    with open('tipos.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tipos_map[int(row['id'])] = row['nome']
    print(f"Dicionário de tipos carregado com sucesso: {tipos_map}")
except FileNotFoundError:
    print("ERRO: Arquivo csv não encontrado.")

@app.route('/', methods=['GET'])
def hello_world():
    """Rota principal que retorna uma mensagem simples.
    Apenas para verificar se a API está no ar.
    """
    return "<p>Olá! Minha API está no ar!</p>"

@app.route("/tipo/<int:tipo_id>")
def get_tipo_por_id(tipo_id):
    """Retorna o nome do tipo correspondente ao ID fornecido.
    Exemplo de uso: /tipo/1
    Retorna: {"id": 1, "nome_tipo": "Tipo A"} ou {"erro": "Tipo com ID 99 não encontrado."}
    Se o ID não existir, retorna uma mensagem de erro com status 404.
    """
    nome_do_tipo = tipos_map.get(tipo_id)

    if nome_do_tipo:
        resposta = {
            "id": tipo_id,
            "nome_tipo": nome_do_tipo
        }
        return jsonify(resposta)
    else:
        resposta_erro = {
            "erro": f"Tipo com ID {tipo_id} não encontrado."
        }
        return jsonify(resposta_erro), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
