from .supermarket import Supermarkets
from datetime import datetime
import pandas as pd
import os

class Devoto(Supermarkets):
    def __init__(self, path_to_cluster_ids, path_to_csv):
        self.api_url: str = "https://www.devoto.com.uy/api/catalog_system/pub/products/search?fq=productClusterIds:"
        self.path_to_cluster_ids = path_to_cluster_ids
        self.path_to_csv = path_to_csv
        super().__init__()
    
    def set_items(self, parsed_res: list):
        for product in parsed_res:
            try:
                product_data = {
                    "cluster_id": self.current_cluster_id,
                    "product_id": product['productId'],
                    "product_name": product['productName'],
                    "brand": product['brand'],
                    "link":product['link'],
                    "listed_price":product['items'][0]['sellers'][0]['commertialOffer']['ListPrice']
                }
                product_dataframe = pd.DataFrame(product_data, index=[0])
                self.products_dataframe = pd.concat([self.products_dataframe, product_dataframe], ignore_index=True)
                print(self.products_dataframe)
            
            except KeyError:
                print(f"Some key was not found in productClusterID {self.current_cluster_id} Leaving empty list...")
                self.cluster_ids_with_errors.append(self.current_cluster_id)
                continue
            
            except Exception as e:
                print(f"General type error at cluter id {self.current_cluster_id}. Leaving empty list...")
                self.cluster_ids_with_errors.append(self.current_cluster_id)
                print(e.args)
                continue               
    
    def save_to_csv(self):
        current_date = datetime.today().toordinal()
        self.products_dataframe.to_csv(
            os.path.join(self.path_to_csv, f"devoto_{current_date}.csv")
        )
        print(self.products_dataframe)
