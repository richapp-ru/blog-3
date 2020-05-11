#!/usr/bin/env python3
import os
import sys

import zmq

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, CUR_DIR)
sys.path.insert(1, os.path.join(CUR_DIR, ".."))

from config import Config
from list_method import listMethod
from item_method import itemMethod
from delete_method import deleteMethod


api = {
    "list": listMethod,
    "item": itemMethod,
    "delete": deleteMethod,
    "undefined": lambda: {"error": "Method key not defined"}
}


def main():
    cfg = Config.get("api")
    ctx = zmq.Context()
    apiSocket = ctx.socket(zmq.REP)
    apiSocket.bind(cfg["apiEndpoint"])

    notifySocket = ctx.socket(zmq.PUB)
    notifySocket.bind(cfg["notifyEndpoint"])

    print("Api listen on {}".format(cfg["apiEndpoint"]))
    print("Api send notifications to {}".format(cfg["notifyEndpoint"]))
    try:
        while True:
            req = apiSocket.recv_json()
            print(">>> {}".format(req))

            method = req.get("method", "undefined")
            params = req.get("params", {})
            res = {
                "id": req.get("id", None),
                "method": method
            }

            try:
                res.update(api[method](params))
            except KeyError:
                res["error"] = "Unexpected method: {}".format(method)

            print(res)
            apiSocket.send_json(res)

            if method == "delete" and "error" not in res:
                notification = {"name": "item.deleted", "data": params}
                print("Send notification:")
                print(notification)
                notifySocket.send_json(notification)
    finally:
        apiSocket.close()
        notifySocket.close()


if __name__ == "__main__":
    main()
