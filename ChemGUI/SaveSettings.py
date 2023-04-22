import json

# dataフォルダが存在しない場合は作成
import os
if not os.path.exists("data"):
    os.mkdir("data")


class SaveSettings:
    def __init__(self, path="data/save.json") -> None:
        self.path = path
        try:
            with open(self.path, 'r') as f:
                self.save_data = json.load(f)
        except:
            self.save_data = {}

    def set(self, key, value):
        self.save_data[key] = value
        # self.save_dataにjson形式で保存
        with open(self.path, 'w') as f:
            json.dump(self.save_data, f, indent=4, ensure_ascii=False)

    def load(self, key):
        if key not in self.save_data:
            return ""
        return self.save_data[key]
