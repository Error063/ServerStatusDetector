import json
import os
import datetime

from flask import Flask, render_template, request
import dbManager

installed = False

app = Flask(__name__)
mgr = dbManager.manager()
if os.path.exists("./config.json"):
    with open("./config.json", mode='r', encoding='utf8') as f:
        info = json.load(f)
        installed = info['installed']


@app.route('/')
def hello_world():
    return render_template("index.html",
                           page=mgr.queryStatus(),
                           title=info['app']['title'],
                           delay=info['detector']['delayTime'],
                           now_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           source=request.referrer
                           )

if __name__ == '__main__':
    if installed:
        app.run()
    else:
        raise Exception("Not installed, please execute setting.py first")