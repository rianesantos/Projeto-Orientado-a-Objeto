from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) # Habilita CORS para permitir requisições do seu frontend React

# Substitua com a sua chave de API da Alpha Vantage
ALPHA_VANTAGE_API_KEY = 'f8fc5b4b559e4e83ad08d8be460d3ce1'
SYMBOL = 'IBM' # Exemplo: Ação da IBM

# Variáveis para simular o alerta
ultimo_preco = None
ALERTA_ATIVO = False

@app.route('/api/data', methods=['GET'])
def get_market_data():
    """
    Endpoint que busca dados de mercado em tempo real da Alpha Vantage
    e verifica se uma condição de alerta foi atingida.
    """
    global ultimo_preco, ALERTA_ATIVO
    
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={SYMBOL}&apikey={ALPHA_VANTAGE_API_KEY}'
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Lança um erro para requisições com status 4xx/5xx
        data = response.json()
        
        # Extrai os dados de interesse
        quote = data.get('Global Quote', {})
        if not quote:
            return jsonify({'error': 'Dados não encontrados ou API offline'}), 404

        preco_atual = float(quote.get('05. price'))
        
        # Lógica para o alerta (simples)
        alerta_disparado = False
        mensagem_alerta = None
        
        # Se for a primeira vez, apenas guarda o preço
        if ultimo_preco is None:
            ultimo_preco = preco_atual
        
        # Verifica se o preço mudou significativamente
        else:
            if abs(preco_atual - ultimo_preco) >= 1.0: # Se o preço subir ou cair mais de 1.00
                mensagem_alerta = f'ALERTA! Preço do {SYMBOL} mudou de {ultimo_preco} para {preco_atual}!'
                alerta_disparado = True
                ultimo_preco = preco_atual
        
        dados_mercado = {
            'symbol': quote.get('01. symbol'),
            'open': quote.get('02. open'),
            'high': quote.get('03. high'),
            'low': quote.get('04. low'),
            'price': preco_atual,
            'volume': quote.get('06. volume'),
            'latest_trading_day': quote.get('07. latest trading day')
        }
        
        return jsonify({
            'data': dados_mercado,
            'alerta': {'disparado': alerta_disparado, 'mensagem': mensagem_alerta}
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na requisição à API: {e}'}), 500
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Erro ao processar os dados: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)