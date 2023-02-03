import json 

def update_dayly_quote_config(file_path="config.json"):
    user_id = str(input("Id:  "))
    set_dayly = input("Dayly :  ")
    doc = {user_id : {"dayly" : str(set_dayly), "when" : "default"}}

    with open(file_path, "r+") as file:
        data = json.load(file)
        dayly_config = data['dayly_quotes_config']
        dayly_config.update(doc)
        data['dayly_quotes_config'] = dayly_config
        print(data)
        file.seek(0)
        json_object = json.dump(data, file, indent=4)
        file.close()

update_dayly_quote_config()