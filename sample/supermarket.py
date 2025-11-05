import requests as req
import pandas as pd
import time
import pickle
import json

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
            "listed_price": []
        })

    def load_cluster_ids(self) -> None:
        with open(self.path_to_cluster_ids, "rb") as plk:
            return pickle.load(plk)

    def request_api(self, cluster_id: int = 1) -> req.Response:
        print(cluster_id)
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
        self.products_dataframe.drop_duplicates(subset='product_id')
