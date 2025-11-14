from context import *
import requests
import time
import pickle
import random
import urllib3
import os
urllib3.disable_warnings()

empty_cluster_ids = []
valid_cluster_ids = []

filepath = os.path.join(ROOT_PATH, "utils")

if os.path.exists(f"{filepath}/empty_cluster_ids.plk"):
	with open(f"{filepath}/empty_cluster_ids.plk", "rb") as file:
		empty_cluster_ids = pickle.load(file)

if os.path.exists(f"{filepath}/valid_cluster_ids.plk"):
	with open(f"{filepath}/valid_cluster_ids.plk", "rb") as file:
		valid_cluster_ids = pickle.load(file)

while True:
	print(empty_cluster_ids, "   \n\n", valid_cluster_ids)
	try:
		i = random.randint(3777, 15000)

		if i in empty_cluster_ids:
			continue

		if i in valid_cluster_ids:
			continue

		print(f"Buscando {i}")

		time.sleep(
			random.randint(2,60)
		)
		res = requests.get(f"https://www.devoto.com.uy/api/catalog_system/pub/products/search?fq=productClusterIds:{i}", verify=False)

		if len(res.content) < 3:
			empty_cluster_ids.append(i)
			continue

		print(f"Encontrado ->{i}")
		valid_cluster_ids.append(i)

	except:
		break

with open(f"{filepath}/valid_cluster_ids.plk", 'wb') as file:
	pickle.dump(valid_cluster_ids, file)
	
with open(f"{filepath}/empty_cluster_ids.plk", 'wb') as file:
	pickle.dump(empty_cluster_ids, file)