from typing import Dict, List
import requests


BANNER_SEARCH_URL = "https://api.criminalip.io/v1/banner/search"
QUERY_LIST = ['tag:Ships']#add query if you want. ex) 'thrane port:10000', 'title:"SAILOR" port:8080', 'title:Thrane &', 'title:"Intellian Aptus Web"', 'SRT Marine Systems', 'title:Furuno'
CRIMINALIP_API_KEY = "<YOUR_API_KEY>"


def criminalip_banner_search_one(query:str, offset:int=0)-> Dict:
	params = {"query": query, "offset": offset}
	headers = {"x-api-key": CRIMINALIP_API_KEY}
	response = requests.get(BANNER_SEARCH_URL, headers=headers, params=params)

	print(response.json())
	return response.json()

def criminalip_banner_search_all(query:str)-> Dict:
	response = criminalip_banner_search_one(query=query, offset=0)
	
	if response['status'] == 200:
		answer = response['data']
		cnt = response['data']['count']
		for i in range(10,cnt,10):
			response = criminalip_banner_search_one(query=query, offset=i)
			if response['status'] == 400:
				break
			answer['result'] += response['data']['result']

		print(answer)
		return answer
	else:
		print(f"API Status:{response['status']}")
		return {'count': 0, 'filters': {}, 'invalid_filters': [], 'result': []}

def criminalip_find_ships(query_list:List[str]=QUERY_LIST):
	output = {}
	for query in query_list:
		print(f'-------------[QUERY]: {query}-------------')
		response = criminalip_banner_search_all(query=query)
		print(response)
		for res in response['result']:
			output[f"{res['ip_address']}:{res['open_port_no']}"] = res
	print("--------------[ANSWER]--------------")
	print(output)
	return output

if __name__ == '__main__':
	criminalip_find_ships()

