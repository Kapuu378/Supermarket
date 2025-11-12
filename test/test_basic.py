from context import *
from sample.devoto import Devoto

devoto = Devoto(
	path_to_cluster_ids = os.path.join(ROOT_PATH, "utils/devoto_cluster_ids.plk"),
	)
print(devoto.path_to_cluster_ids)
for id in devoto.cluster_ids:
	res = devoto.request_api(id)
	#parsed_res = devoto.parse_api_res(raw_res)
	devoto.set_items(res)
	print(id)

devoto.remove_duplicates()
devoto.upload_to_db()