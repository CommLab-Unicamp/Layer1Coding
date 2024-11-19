'''
 * Simulador de Comunicação
 * 
 * Participantes: Rafael Ifanger Ribeiro, Y, Z
 * Período: Segundo Semestre de 2024
 * Disciplina: EE881
 * 
 * Descrição:
 * Este script implementa a lógica para o simulador de comunicação, incluindo o envio de dados
 * para o backend, atualização de tabelas e gráficos, e geração de texto aleatório para simulação.
 * 
 * Funções Principais:
 * - Gerar texto aleatório.
 * - Enviar dados para o backend.
 * - Atualizar tabela de resultados.
'''

from flask import Flask, render_template, request, jsonify
from aplicacao_modelo import executar_modelo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/processar', methods=['POST'])
def processar_endpoint():
    data = request.json
    vetor_entrada_char = data['vetor_entrada']
    variancia = float(data['variancia'])
    resultado = executar_modelo(vetor_entrada_char, variancia)
    resultado['variancia'] = variancia
    print(resultado)
    return jsonify(resultado)


if __name__ == '__main__':
    app.run(debug=True)
