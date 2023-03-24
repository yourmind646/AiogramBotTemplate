import simplejson as json

# init
CFG_PATH = "cfg/config.json"


# load cfg and return it
def load_config(cfg_path = CFG_PATH):

	with open(cfg_path, "r", encoding = "utf-8") as config_fp:
		return json.load(config_fp)
