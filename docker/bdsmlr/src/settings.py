import os
import random


THIS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))

IMG_DIR = os.path.join(THIS_DIR, "images")

MANAGER_URL = "http://manager:6969"

PUBLISHER_URL = "http://publisher:6969"


def random_user_agent():
    with open(os.path.join(THIS_DIR, "data", "user-agents.txt"), "r") as ts:
        ua = random.choice([x.strip("\n") for x in ts.readlines()])
        ts.close()
    return ua
