from flask import Flask, render_template, request
from flask import jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    name = "who"
    #return name
    return render_template('hello.html', title='hello2', name=name)

@app.route('/get_joycon_L_data')
def get_L():
    f = open('./joyCon/L_data.txt')
    L_data = int(f.readline()) 
    return jsonify({'L_data':L_data})

@app.route('/get_joycon_data')
def get_data():
    joycon_data = requests.get('https://script.google.com/macros/s/AKfycbzCa4Xp_WHXIziduPKaa8kOZ_ZR9qc-XxWHMY0bcuLGYDXArojT/exec')
    joycon_data = joycon_data.json()

    return jsonify({"player0":joycon_data['player0'],"player1":joycon_data['player1']})

@app.route('/websocket')
def blue():
    value = "who"
    #return name
    return render_template('socket.html', title='hello2', value=value)

if __name__ == "__main__":
    joycon_data = requests.get('https://script.google.com/macros/s/AKfycbzCa4Xp_WHXIziduPKaa8kOZ_ZR9qc-XxWHMY0bcuLGYDXArojT/exec')
    print(joycon_data)
    app.run(debug=True, port=8888, threaded=True)
