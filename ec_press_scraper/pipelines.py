import json
from pathlib import Path

from itemadapter import ItemAdapter


class JsonlWriterPipeline:
    def open_spider(self, spider):
        Path("data").mkdir(exist_ok=True)
        self.file = open("data/press_releases.jsonl", "w", encoding="utf-8")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        line = json.dumps(adapter.asdict(), ensure_ascii=False)
        self.file.write(line + "\n")
        return item
