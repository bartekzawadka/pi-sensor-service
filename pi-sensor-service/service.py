#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import json
from runner import SensorsRunner

app = flask.Flask(__name__)

sRunner = SensorsRunner()
sRunner.start()


@app.route('/get_temp_hum')
def get_temp_hum():
    return json.dumps(sRunner.get_last_results())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=888, debug=False)