import os

from config import Config


def listMethod(params):
    if "year" not in params:
        return {"result": {"years": os.listdir(Config.DATA_DIR)}}
    if "month" not in params:
        yearDir = os.path.join(Config.DATA_DIR, params["year"])
        if os.path.exists(yearDir):
            return {"result": {"months": os.listdir(yearDir)}}
        else:
            return {"error": "Not exists: year={}".format(params["year"])}
    if "day" not in params:
        monthDir = os.path.join(
            Config.DATA_DIR,
            params["year"],
            params["month"]
        )
        if os.path.exists(monthDir):
            return {"result": {"days": os.listdir(monthDir)}}
        else:
            return {"error": "Not exists: year={}, month={}".format(
                params["year"],
                params["month"]
            )}
    if "hour" not in params:
        dayDir = os.path.join(
            Config.DATA_DIR,
            params["year"],
            params["month"],
            params["day"]
        )
        if os.path.exists(dayDir):
            return {"result": {"hours": os.listdir(dayDir)}}
        else:
            return {"error": "Not exists: year={}, month={}, day={}".format(
                params["year"],
                params["month"],
                params["day"]
            )}
    if "minute" not in params:
        hourDir = os.path.join(
            Config.DATA_DIR,
            params["year"],
            params["month"],
            params["day"],
            params["hour"]
        )
        if os.path.exists(hourDir):
            return {"result": {"minutes": os.listdir(hourDir)}}
        else:
            return {"error": "Not exists: year={}, month={}, day={}, hour={}".format(
                params["year"],
                params["month"],
                params["day"],
                params["hour"]
            )}

    minuteDir = os.path.join(
        Config.DATA_DIR,
        params["year"],
        params["month"],
        params["day"],
        params["hour"],
        params["minute"]
    )
    if os.path.exists(minuteDir):
        return {"result": {"packets": sorted([int(item[7:-5]) for item in os.listdir(minuteDir)])}}
    else:
        return {"error": "Not exists: year={}, month={}, day={}, hour={}, minute={}".format(
            params["year"],
            params["month"],
            params["day"],
            params["hour"],
            params["minute"]
        )}
