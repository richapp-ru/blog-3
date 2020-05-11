import os
import yaml

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CUR_DIR, ".."))
CONFIG_PATH = os.path.join(ROOT_DIR, "etc", "config.yaml")


class Config(object):
    ROOT_DIR = ROOT_DIR
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    BATCH_SIZE = 1000
    MIN_IPADDRESS = 0
    MAX_IPADDRESS = 2**32 - 1
    MIN_BYTES = 0
    MAX_BYTES = 100 * 1024 * 1024
    IFACES = ["eth{}".format(i) for i in range(8)]

    _instance = None

    @classmethod
    def get(cls, sectionName):
        if cls._instance is None:
            if not os.path.exists(CONFIG_PATH):
                print("HINT: cp {}/example-config.yaml {}".format(os.path.dirname(CONFIG_PATH), CONFIG_PATH))
                raise Exception("Config not exists: {}".format(CONFIG_PATH))

            with open(CONFIG_PATH) as fstream:
                cls._instance = yaml.load(fstream)

        return cls._instance[sectionName]
