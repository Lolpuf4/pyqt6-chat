import json
import datetime


def save_cookie(username, password):
    file_info = {
        "username": username,
        "password": password,
        "date": datetime.date.today().strftime("%Y/%m/%d")
    }
    with open("jsons/cookie.json", "w", encoding="UTF-8") as f:
        json.dump(file_info, f)