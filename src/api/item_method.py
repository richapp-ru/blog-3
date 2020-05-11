import os
import json

from config import Config


def itemMethod(params):
    if (   "year" not in params
        or "month" not in params
        or "day" not in params
        or "hour" not in params
        or "minute" not in params
        or "num" not in params):
        return {"error": "Parameters year, month, day, hour, minute, num must exists"}

    path = os.path.join(
        Config.DATA_DIR,
        params["year"],
        params["month"],
        params["day"],
        params["hour"],
        params["minute"],
        "packet-{}.json".format(params["num"])
    )
    if os.path.exists(path):
        with open(path) as fstream:
            return {"result": json.load(fstream)}
    else:
        return {"error": "Not exists: year={}, month={}, day={}, hour={}, minute={}, num={}".format(
            params["year"],
            params["month"],
            params["day"],
            params["hour"],
            params["minute"],
            params["num"]
        )}
