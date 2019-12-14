from flask import Flask, render_template, request
from flask import jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    name = "who"
    #return name
    return render_template('hello.html', title='hello2', name=name)

@app.route('/get_joycon_data')
def get_data():
    joycon_data = requests.get('https://script.google.com/macros/s/AKfycbzCa4Xp_WHXIziduPKaa8kOZ_ZR9qc-XxWHMY0bcuLGYDXArojT/exec')
    joycon_data = joycon_data.json()
    player0 = joycon_data[0][0]
    player1 = joycon_data[0][1]
    joycon0 = joycon_data[1][0]
    joycon1 = joycon_data[1][1]

    return jsonify({player0:joycon0,player1:joycon1})

@app.route('/bluetoothtest')
def blue():
    value = "who"
    #return name
    return render_template('blue.html', title='hello2', value=value)

if __name__ == "__main__":
    joycon_data = requests.get('https://script.google.com/macros/s/AKfycbzCa4Xp_WHXIziduPKaa8kOZ_ZR9qc-XxWHMY0bcuLGYDXArojT/exec')
    print(joycon_data)
    app.run(debug=True, port=8888, threaded=True)
