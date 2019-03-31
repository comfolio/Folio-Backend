from flask import Flask, jsonify, request
from flask_cors import CORS

from fuzzywuzzy import fuzz, process

import io

app = Flask(__name__, static_url_path='/../../Comfolio-Frontend')
CORS(app)

def parse_ticket_symbol_file(filename):
    symbol_map = {}
    with open(filename) as file:
        raw_lines = [line.strip() for line in file.readlines() if len(line.strip()) != 0]

    for line in raw_lines:
        (symbol, name) = line.split('\t')
        symbol_map[symbol] = name

    return symbol_map

def save_to_tmp_file():
    sio = io.BytesIO()
    plt.savefig(sio, format='png')
    sio.seek(0)
    buffer = sio.getvalue()
    b64 = base64.b64encode(buffer)

    return b64

# nyse_data = parse_ticket_symbol_file('./ticker-symbols/NYSE.txt')
nasdaq_data = parse_ticket_symbol_file('./ticker-symbols/NASDAQ.txt')
all_ticker_data = {
    # **nyse_data,
    **nasdaq_data
}
all_symbols = all_ticker_data.keys()

@app.route('/ticker-symbol-search', methods=['GET'])
def search_ticker_symbols():
    symbol = request.args.get('symbol')
    max_limit = request.args.get('limit', type=int, default=5)
    likely_candidates = process.extract(symbol, all_symbols, limit=max_limit)
    likely_symbols = [candidate[0] for candidate in likely_candidates]
    return jsonify(likely_symbols)

@app.route('/ticker-symbols', methods=['GET'])
def get_tsymbol_list():
    nyse_data = parse_ticket_symbol_file('./ticker-symbols/NYSE.txt')
    nasdaq_data = parse_ticket_symbol_file('./ticker-symbols/NASDAQ.txt')
    return jsonify({ **nyse_data, **nasdaq_data })

@app.route('/generate-graph', methods=['GET'])
def generate_graph():
    import json
    input_tickers = json.loads(request.args.get('params').replace('%22', ''))
    image_dict = GraphMaker(input_tickers)
    print(image_dict)
    return jsonify(image_dict['full'].decode("utf-8"))

@app.route('/generate-pie', methods=['GET'])
def generate_pie():
    import json
    input_tickers = json.loads(request.args.get('params'))
    image_dict = GraphMaker(input_tickers)
    print(image_dict)
    return jsonify(image_dict['full'].decode("utf-8"))

@app.route('/get-leaderboard', methods=['GET'])
def get_leaderboard():
    pass

@app.route('/get-portfolio', methods=['GET'])
def get_portfolio():
    pass

@app.route('/update-portfolio', methods=['POST'])
def update_portfolio():
    pass

from GraphMaker import GraphMaker
from PieMaker import PieMaker

if __name__ == '__main__':
    #GraphMaker({"GOOGL":50, "NFLX":20, "FB":20, "AMZN":10})
    # , "FB":20, "AMZN":10
    # PieMaker({"AAPL":25, "VWO":25, "AGG":25, "MALOX":25})
    app.run(debug=True, port=8080)