from context import *
import requests as req
import pandas as pd
import time
import pickle
import json

from MySQLdb import _mysql
from dotenv import load_dotenv
import os

load_dotenv(
    dotenv_path=os.path.join(
        ROOT_PATH, 'utils/sql_credentials.env')
)
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

class Supermarkets:
    def __init__(self):
        self.request: object = req.Session()
        self.current_cluster_id: int = None
        self.cluster_ids: list[int] = self.load_cluster_ids()
        self.cluster_ids_with_errors: list[int] = []
        self.products_dataframe = pd.DataFrame(data={
            "cluster_id": [],
            "product_id": [],
            "product_name": [],
            "brand": [],
            "link": [],
            "listed_price": [],
            "supermarket_name": [],
            "date": []
        })

    def load_cluster_ids(self) -> None:
        with open(self.path_to_cluster_ids, "rb") as plk:
            return pickle.load(plk)

    def request_api(self, cluster_id: int = 1) -> req.Response:
        time.sleep(0.35)
        self.current_cluster_id = cluster_id
        api_response = self.request.get(self.api_url + str(cluster_id), verify=False)
        parsed_api_res = self.parse_api_res(api_response)
        return parsed_api_res

    def parse_api_res(self, api_res: req.Response) -> dict:
        api_string = api_res.content
        parsed_res = json.loads(api_string)
        return parsed_res

    def remove_duplicates(self) -> None:
        self.products_dataframe.drop_duplicates(subset='product_id', inplace=True)

    def upload_to_db(self):
        for index, row in self.products_dataframe.iterrows():
            db =_mysql.connect(
                "FranciscoGibert.mysql.pythonanywhere-services.com",
                USERNAME,
                PASSWORD,
                "FranciscoGibert$prices"
            )
            db.query(f"""
            INSERT INTO products(cluster_id, product_id, product_name, brand, link, listed_price, supermarket_name, date)
            VALUES({row['cluster_id']},{row['product_id']},'{row['product_name']}','{row['brand']}','{row['link']}',{row['listed_price']},'{row['supermarket_name']}','{row['date']}'
            );""")



