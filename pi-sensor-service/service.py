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


@app.route('/get_last_pwm')
def get_last_pwm():
    return json.dumps({'pwm': sRunner.get_last_pwm()})


@app.route('/set_pwm/')
def set_pwm():
    pwmString = flask.request.args.get('pwm')
    if pwmString is not None:
        try:
            pwm = int(pwmString)
        except Exception, e:
            return json.dumps({'success': False, 'error': 'Cannot parse input value to integer'}), 200, {
                'ContentType': 'application/json'}
        else:
            sRunner.set_fans_speed(pwm)
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False, 'error': 'Cannot parse input value to integer'}), 200, {'ContentType': 'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=888, debug=False)