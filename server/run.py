from flask import Flask, jsonify, request
from flask_cors import CORS

from fuzzywuzzy import fuzz, process

import json
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

@app.route('/full-graph')
def get_full_graph():
    with open('user-data.json', 'r') as infile:
        input_tickers = json.load(infile)

    image_dict = GraphMaker(input_tickers)
    full_img = image_dict['full'].decode("utf-8")
    return jsonify(full_img)

@app.route('/generate-graph', methods=['GET'])
def generate_graph():
    input_tickers = json.loads(request.args.get('params').replace('%22', ''))

    print(input_tickers)

    with open('user-data.json', 'w') as outfile:
        json.dump(input_tickers, outfile)

    start_epoch = request.args.get('epoch', type=int, default=-1)
    if start_epoch != -1:
        image_dict = GraphMaker(input_tickers, startdate = start_epoch)
    else:
        image_dict = GraphMaker(input_tickers)

    final_dict = {
        '30-days': image_dict['30'].decode("utf-8"),
        '90-days': image_dict['90'].decode("utf-8"),
        '150-days': image_dict['150'].decode("utf-8"),
        '360-days': image_dict['360'].decode("utf-8"),
        'full-days': image_dict['full'].decode("utf-8")
    }

    return jsonify(final_dict)

@app.route('/generate-pie', methods=['GET'])
def generate_pie():
    input_tickers = json.loads(request.args.get('params').replace('%22', ''))
    image = PieMaker(input_tickers)
    return jsonify(image.decode("utf-8"))

from GraphMaker import GraphMaker
from PieMaker import PieMaker

if __name__ == '__main__':
    #GraphMaker({"GOOGL":50, "NFLX":20, "FB":20, "AMZN":10})
    # , "FB":20, "AMZN":10
    # PieMaker({"AAPL":25, "VWO":25, "AGG":25, "MALOX":25})
    app.run(debug=True, port=8080)