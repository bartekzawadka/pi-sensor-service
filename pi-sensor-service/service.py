import flask
import json
import Adafruit_DHT

app = flask.Flask(__name__)


@app.route('/get_temp_hum')
def get_temp_hum():
    result = {}

    h1,t1 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)
    h2,t2 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 24)

    if h1 is not None and t1 is not None:
        result['Sensor1'] = {}
        result['Sensor1']['temperature'] = '{0:0.1f}'.format(t1)
        result['Sensor1']['humidity'] = '{0:0.1f}'.format(h1)

    if h2 is not None and t2 is not None:
        result['Sensor2'] = {}
        result['Sensor2']['temperature'] = '{0:0.1f}'.format(t2)
        result['Sensor2']['humidity'] = '{0:0.1f}'.format(h2)

    return json.dumps(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=888, debug=False)