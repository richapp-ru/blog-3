#!/usr/bin/env python3
import os
import sys
import logging
import multiprocessing
from time import sleep

import zmq
from termcolor import cprint

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(CUR_DIR, ".."))

from config import Config


def help():
    print("list(<year>, <month>, <day>, <hour>, <minute>)")
    print("# Получение списка блоков данных за минуту 2020-05-11 21:28")
    print(">>> list(2020, 5, 11, 21, 28)")
    print("# Получение списка месяцев с данными в 2020 году")
    print(">>> list(2020)")
    print("# Получение списка годов с данными")
    print(">>> list()")
    print("")
    print("item(<year>, <month>, <day>, <hour>, <minute>, <num>)")
    print("# Получение блока номер 0 из минуты 2020-05-11 21:28")
    print(">>> item(2020, 5, 11, 21, 28, 0)")
    print("")
    print("delete(<year>, <month>, <day>, <hour>, <minute>, <num>)")
    print("# Удаления блока номер 0 из минуты 2020-05-11 21:28")
    print(">>> delete(2020, 5, 11, 21, 28, 0)")

keys = ["year", "month", "day", "hour", "minute", "num"]


def parseParams(params):
    result = {}
    for num, item in enumerate(params):
        if not item:
            continue

        try:
            if keys[num] == "num":
                result["num"] = str(int(item.strip())).rjust(8, "0")
            else:
                result[keys[num]] = str(int(item.strip())).rjust(2, "0")
        except ValueError:
            cprint("Expect {} type int, value={}".format(keys[num], item.strip()))
            continue
        except IndexError:
            cprint("Error: Too many params", "red")
            continue
    return result


def notifyProcess():
    cfg = Config.get("client")
    ctx = zmq.Context()

    notifySocket = ctx.socket(zmq.SUB)
    notifySocket.setsockopt(zmq.SUBSCRIBE, b"")
    notifySocket.connect(cfg["notifyEndpoint"])

    print("Client connected to notify channel {}".format(cfg["notifyEndpoint"]))
    try:
        while True:
            message = notifySocket.recv_json()
            print("")
            print("Notification received")
            print(message)
    except Exception as e:
        cpint(e, "red")
    finally:
        notifySocket.close()


def main():
    cfg = Config.get("client")
    ctx = zmq.Context()

    apiSocket = ctx.socket(zmq.REQ)
    apiSocket.connect(cfg["apiEndpoint"])

    print("Client connected to API at {}".format(cfg["apiEndpoint"]))

    notify = multiprocessing.Process(target=notifyProcess)
    notify.start()
    sleep(0.1)

    cmdId = 0
    print(">>> \\q - Выход")
    print(">>> \\h - Описание комманд")
    try:
        while True:
            cmd = input(">>> ").strip()
            sys.stdout.flush()

            if cmd == "\\q":
                print("Quit")
                break
            elif cmd == "\\h":
                help()
                continue
            elif cmd.startswith("list"):
                method = "list"
                params = parseParams(cmd[4:].strip(" ()").split(","))

            elif cmd.startswith("item"):
                method = "item"
                params = parseParams(cmd[4:].strip(" ()").split(","))
                if len(params) < len(keys):
                    cprint("Expected len(params) == {}".format(len(keys)))
            elif cmd.startswith("delete"):
                method = "delete"
                params = parseParams(cmd[6:].strip(" ()").split(","))
                if len(params) < len(keys):
                    cprint("Expected len(params) == {}".format(len(keys)))
            else:
                cprint("Unexpected command: `{}`".format(cmd), "red")
                continue

            cmdId += 1
            apiSocket.send_json({
                "id": cmdId,
                "method": method,
                "params": params
            })
            res = apiSocket.recv_json()

            if "error" in res:
                cprint(res, "red")
                continue

            if method == "item":
                result = res["result"]
                res["result"] = "len(result) = {}".format(len(result))
                print(res)
                for item in result[:10]:
                    print(item)
                print("...")
                print("... Skipped {}".format(len(result) - 20))
                print("...")
                for item in result[-10:]:
                    print(item)
            else:
                print(res)
    finally:
        notify.terminate()
        apiSocket.close()

if __name__ == "__main__":
    main()
