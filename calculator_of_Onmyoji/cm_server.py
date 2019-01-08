#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback

import flask
import json

from tempfile import mkdtemp

from calculator_of_Onmyoji import cal_mitama
from calculator_of_Onmyoji.data_format import MITAMA_TYPES, MITAMA_PROPS

tmp_folder = mkdtemp()

app = flask.Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html',
                                 mitama_types=MITAMA_TYPES,
                                 mitama_props=MITAMA_PROPS)


@app.route('/calculate', methods=['POST', 'OPTIONS'])
def calculate():
    try:
        if flask.request.method == 'OPTIONS':
            resp = flask.current_app.make_default_options_response()
            h = resp.headers

            h['Access-Control-Allow-Origin'] = '*'
            h['Access-Control-Allow-Methods'] = 'POST'
            h['Access-Control-Allow-Headers'] = "Content-Type,\
             Access-Control-Allow-Headers, Authorization, X-Requested-With"
            return resp
        elif flask.request.method == 'POST':
            if flask.request.is_json:
                json_request = flask.request.get_json()
            else:
                form_request = flask.request.form
                json_request = {}
                for key in form_request:
                    json_request[key] = json.loads(form_request[key])

            f = flask.request.files['mitama_file']
            save_path = tmp_folder+'/'+json_request['file_name']
            f.save(save_path)
            json_request['file_name'] = save_path
            calculator = cal_mitama.Calculator(json_request)
            calculator.run()

            return 'Calculate finished'
    except Exception:
        return traceback.format_exc()


if __name__ == '__main__':
    # TODO(jjs): load host and port from config file
    app.run(host='0.0.0.0', port=2019)
