from flask import Flask, render_template, request
from flask import jsonify

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

@app.route('/websocket')
def blue():
    value = "who"
    #return name
    return render_template('socket.html', title='hello2', value=value)

if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)
