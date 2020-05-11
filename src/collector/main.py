#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime

import zmq
from termcolor import cprint

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(CUR_DIR, ".."))

from config import Config


def main():
    cfg = Config.get("collector")
    ctx = zmq.Context()

    socket = ctx.socket(zmq.PULL)
    socket.bind(cfg["collectorEndpoint"])

    num = 0
    print("Collector listen on {}".format(cfg["collectorEndpoint"]))

    try:
        while True:
            packet = socket.recv_json()

            if len(packet) == 0 or type(packet) != list:
                continue

            timeObject = datetime.fromtimestamp(packet[0]["time"])
            (
                year,
                month,
                day,
                hour,
                minute
            ) = timeObject.strftime("%Y-%m-%d-%H-%M").split("-")
            dstDir = os.path.join(Config.DATA_DIR, year, month, day, hour, minute)

            if not os.path.exists(dstDir):
                os.makedirs(dstDir)

            packetNum = len(os.listdir(dstDir))

            with open(os.path.join(dstDir, "packet-{}.json".format(str(packetNum).rjust(8, "0"))), "w") as fstream:
                fstream.write(json.dumps(packet))

            num += 1
            if num % 100 == 0:
                print("Packets received: {}".format(num))
    finally:
        socket.close()


if __name__ == "__main__":
    main()
