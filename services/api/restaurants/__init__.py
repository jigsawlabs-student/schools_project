from flask import Flask, jsonify
import os


app = Flask(__name__)


@app.route('/restaurants')
def locations():
    locations = [
            {'id': 1, 'name': 'chipotle', 'address': '3rd and 7th ave'},
            {'id': 2, 'name': 'famiglia', 'address': '12th and 8th ave'},
            ]
    return jsonify({'locations': locations})