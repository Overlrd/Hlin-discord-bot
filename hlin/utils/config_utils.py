import logging
import json 
from settings import CONFIG_FILE_PATH , DEFAULT_CONFIG

def load_config_for_user(user_id="all", file_path="config.json", config="dayly_quotes_config"):
    logging.info("utils-load_config_for_user - loading user config from file")
    with open(file_path, "r") as file:
        data = json.load(file)
    cfg = data.get(config, {})
    if user_id == "all":
        return cfg
    else:
        return cfg.get(str(user_id), {})



## update or create config for dayly quote
def update_dayly_quote_config(user_id,dayly, when,file_path = CONFIG_FILE_PATH.absolute(), config=DEFAULT_CONFIG, **kwargs):
    logging.info("utils-update_dayly_quote_config - update dayly quote in users config file")
    doc = {str(user_id): {"dayly": dayly, "when": str(when)}}
    with open(file_path, "r") as file:
        data = json.load(file)
    cfg = data[config]
    cfg.update(doc)
    for i in kwargs :
        cfg.update({'{}'.format(i):kwargs.get(i)})
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    return doc
