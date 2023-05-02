import logging
import json 


def load_config_for_user(user_id="all", file_path="config.json"):
    logging.info("utils-load_config_for_user - loading user config from file")
    try :
        with open(file_path, "r") as file:
            data = json.load(file)
            dayly_config = data.get('dayly_quotes_config', {})
            if user_id == "all":
                # Return a dictionary of user IDs and configurations
                return {user_id: json.loads(config) if isinstance(config, str) else config for user_id, config in dayly_config.items()}
            else:
                return dayly_config.get(str(user_id), {})
    except Exception as e:
       logging.error(f"{e}")


## update or create config for dayly quote
def update_dayly_quote_config(user_id, set_dayly, when="none", file_path="config.json"):
    logging.info("utils-update_dayly_quote_config - update dayly quote in users config file")
    doc = {str(user_id): {"dayly": str(set_dayly), "when": str(when)}}
    with open(file_path, "r") as file:
        data = json.load(file)
        dayly_config = data['dayly_quotes_config']
        dayly_config.update(doc)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    if set_dayly:
        message = f"Daily quotes have been activated for {when}."
    else:
        message = "Daily quotes have been deactivated."
    return message
