from context import *
from sample.devoto import Devoto
from dotenv import load_dotenv
import os

load_dotenv(
    dotenv_path=os.path.join(
        ROOT_PATH, 'utils/sql_credentials.env')
)

MY_ENV_VAR = os.getenv('TEST')
print(MY_ENV_VAR)

devoto = Devoto(
	path_to_cluster_ids = os.path.join(ROOT_PATH, "utils/devoto_cluster_ids.plk"),
	path_to_csv = CSV_PATH
				)
print(devoto.path_to_cluster_ids)
for id in devoto.cluster_ids:
	res = devoto.request_api(id)
	#parsed_res = devoto.parse_api_res(raw_res)
	devoto.set_items(res)
	print(id)

devoto.remove_duplicates()
devoto.save_to_csv()