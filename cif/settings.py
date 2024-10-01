import os


PATH_BASE = os.path.dirname(__file__).rsplit("/", 1)[0]
PATH_SERVICES = os.path.join(PATH_BASE, "services")
PATH_ACTIONS = os.path.join(PATH_BASE, "actions")
PATH_BUILD = os.path.join(PATH_BASE, ".build")
