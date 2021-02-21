import requests
from bs4 import BeautifulSoup
import json

# personUrlList = []

# for i in range(0, 740, 20):
# 	url = f"https://www.bundestag.de/ajax/filterlist/en/members/453158-453158?limit=20&noFilterSet=true&offset={i}"

# 	req = requests.get(url)
# 	result = req.content
# 	soup = BeautifulSoup(result, 'lxml')

# 	persons = soup.find_all(class_ = 'bt-open-in-overlay')

# 	for person in persons:
# 		personPageUrl = person.get("href")
# 		personUrlList.append(personPageUrl)
# with open('personUrlList.txt', "w", encoding='utf-8') as file:
# 	for line in personUrlList:
# 		file.write(f'{line}\n')
with open('personUrlList.txt', 'r', encoding='utf-8') as file:
	lines = [line.strip() for line in file.readlines()]

	dataDict = []
	count = 0

	for line in lines:
		q = requests.get(line)
		result = q.content

		soup = BeautifulSoup(result, 'lxml')
		person = soup.find(class_='bt-biografie-name').find('h3').text

		personNameCompany = person.strip().split(',')
		personName = personNameCompany[0]
		personCompany = personNameCompany[1].strip()

		sotialNetworks = soup.find_all(class_='bt-link-extern')

		socialNetworkUrls = []
		for item in sotialNetworks:
			socialNetworkUrls.append(item.get('href'))
		
		data = {
			'personName':personName,
			'personCompany': personCompany,
			'socialNetworks': socialNetworkUrls
		}
		count+=1
		print(f'#{count}: {line} is done')

		dataDict.append(data)

		with open('data.json', "a", encoding='utf-8') as file:
			json.dump(dataDict, file, indent=4)