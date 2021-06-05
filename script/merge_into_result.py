import json

with open("crawled.json", "r", encoding="UTF-8") as f:
    crawled_data = json.loads(f.read())

with open("result-korean-character.json", "r", encoding="UTF-8") as f:
    charactors_json = json.loads(f.read())


for k, v in list(crawled_data.items()):
    if (
        input(
            f"Are you sure you want to overwrite that?\n\nkey: {k}\nvalue: {v}\n\n"
        ).lower()
        == "y"
    ):
        charactors_json[k] = v
    else:
        pass

with open("merged.json", "w", encoding="UTF-8") as f:
    crawled_data = f.write(json.dumps(charactors_json, ensure_ascii=False))
