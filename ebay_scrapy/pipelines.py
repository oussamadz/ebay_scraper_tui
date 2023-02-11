# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class EbayScrapyPipeline:
    def process_item(self, item, spider):
        conn = sqlite3.connect("db.sqlite3")
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM ITEMS WHERE id={item['prodId']} AND task={item['task']};")
        data = cur.fetchone()
        if not data:
            title = item['title'].replace("'", " ").replace(
                ",", "").replace("\n", " ").replace("\t", " ")
            cur.execute(
                f"INSERT INTO ITEMS (id, title, url, condition, price, sell, shipping, task) VALUES ({item['prodId']}, '{title}', '{item['url']}', '{item['condition']}', '{item['price']}', '{item['sell']}', '{item['shipping']}', {item['task']});")
        else:
            cur.execute(
                f"UPDATE ITEMS SET title = '{title}', price = '{item['price']}', condition = '{item['condition']}', sell = '{item['sell']}', shipping = '{item['shipping']}' WHERE id = {item['prodId']};")

        conn.commit()
        cur.close()
        conn.close()
        return item
