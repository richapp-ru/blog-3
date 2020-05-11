#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime
import yaml
import zmq

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(CUR_DIR, ".."))

from config import Config


def main():
    cfg = Config.get("adapter")
    ctx = zmq.Context()

    adapterSocket = ctx.socket(zmq.PULL)
    adapterSocket.bind(cfg["adapterEndpoint"])

    collectorSocket = ctx.socket(zmq.PUSH)
    collectorSocket.connect(cfg["collectorEndpoint"])

    num = 0
    print("Adapter listen on {}".format(cfg["adapterEndpoint"]))
    print("Adapter push to collector {}".format(cfg["collectorEndpoint"]))
    try:
        while True:
            packet = adapterSocket.recv().decode()

            data = []
            for line in packet.split("\n"):
                split = line.split("\t")
                data.append({
                    "time": float(split[0]),
                    "ip": split[1],
                    "bytes_sent": int(split[2]),
                    "bytes_received": int(split[3]),
                    "iface": split[4]
                })

            collectorSocket.send_json(data)

            num += 1
            if num % 100 == 0:
                print("Packets sent: {}".format(num))
    finally:
        adapterSocket.close()
        collectorSocket.close()


if __name__ == "__main__":
    main()
