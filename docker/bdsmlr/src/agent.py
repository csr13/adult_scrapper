import datetime
import json
import logging
import os
import subprocess
import sys
import time

import requests
from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler

from logger import get_logger
from environment import Environment
from settings import THIS_DIR, MANAGER_URL, PUBLISHER_URL


app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start(paused=False)


logger = get_logger(__name__)


Env = Environment()


##########################################################
# Cron Tasks and Declarations.
##########################################################

@scheduler.task(
    'cron',
    id='update_env_blogs',
    minute="*/1"
)
def update_env_blogs():
    Env.load_blogs_from_manager()
    return True



##############################################################
# API Endpoints
##############################################################


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify(
        message="pong"
    ), 200


@app.route("/on-off", methods=["POST"])
def switch_env():
    status = request.form.get("status")
    if status is None:
        return jsonify(message="Missing status"), 400
    if status.lower() not in ["on", "off"]:
        return jsonify(message="status not one of on|off"), 400
    op = Env.on_switch(status)
    if op:
        if status == "on": 
            # schedulerstate is 1
            scheduler.resume()
        elif status == "off": 
            # scheduler state is 2
            scheduler.pause()
        return jsonify(
            message="Status: %s" % status
        ), 200
    return jsonify(
        message="Unable to change status"
    ), 400


@app.route("/env-stats", methods=["GET"])
def env_stats():
    data = {
        "env" : {
            "on" : True if not Env.on else False,
            "runs" : Env.runs,
            "loaded_blogs" : Env.blogs,
            "start_time" : Env.start_time,
            "settings" : {
                "max_images" : Env.max_images,
                "streak_limit" : Env.streak_limit
            }
        }
    }
    return jsonify(
        data=data
    ), 200



@app.route("/get-attr/<attr>", methods=["GET"])
def get_attr(attr):
    if hasattr(Env, attr):
        attr = Env.__getattribute__(attr)
    else:
        attr = ''
    return jsonify(attr=attr), 200


#####################################################
# Event RPC Endpoints.
#####################################################


@app.route("/update-env-blogs", methods=["POST"])
def update_env_blogs():
    logger.info("Signal to update blogs received from manager.")
    Env.load_blogs_from_manager()
    return jsonify(status=True), 200


@app.route("/bulk-runs", methods=["POST"])
def bulk_runs():
    data = request.form.getlist("uids")
    scrapes = []
    for each in data:
        check = Env.single_run(each)
        scrapes.append(check[1])
    return jsonify(
        success=True, 
        scrapes_data=scrapes
    ), 200


@app.route("/manual-run/single/<blog_uid>", methods=["POST"])
def single_run(blog_uid):
    check = Env.single_run(blog_uid)
    if not check[0]:
        success = False
        status = 400
    else:
        success = True
        status = 200
    run_data = check[1]
    return jsonify(
        success=success, 
        scrape_data=run_data
    ), status


def main():
    if Env.on:
        status = 'on'
    else:
        status = 'off'
    logger.info("BDSML FEED started, current status: %s " % status)
    app.run(
        debug=True, 
        host="0.0.0.0", 
        port=8888
    ) 


if __name__ == "__main__":
    main()
