from bs4 import BeautifulSoup
import requests
import json
import csv
from time import sleep
import random

# url = "https://health-diet.ru/table_calorie/"
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
}
# req = requests.get(url, headers=headers)

# src=req.text
# with open("index.html", "w", encoding="utf-8") as file:
# 	file.write(src)

# with open("index.html", encoding="utf-8") as file:
# 	src = file.read()

# soup = BeautifulSoup(src, "lxml")

# allCategoriesDict = {}
# allProdutsHrefs = soup.find_all(class_="mzr-tc-group-item-href")
# for item in allProdutsHrefs:
# 	itemText = item.text
# 	itemHref = "https://health-diet.ru"+item.get("href")

# 	allCategoriesDict[itemText] = itemHref

# with open("allCategoriesDict.json", "w", encoding="utf-8") as file:
# 	json.dump(allCategoriesDict, file, indent=4, ensure_ascii=False)

with open("allCategoriesDict.json", "r", encoding="utf-8") as file:
	allCategories = json.load(file)

iterationCount = int(len(allCategories))
count = 0
print(f"Total iterations: {iterationCount}")

for categoryName, categoryHref in allCategories.items():
	rep = [",", " ", "-", "'"]
	for item in rep:
		if item in categoryName:
			categoryName = categoryName.replace(item, "_")
	
	req = requests.get(url = categoryHref, headers = headers)
	src = req.text

	with open(f"data/{count}_{categoryName}.html", "w", encoding="utf-8") as file:
		file.write(src)
		
	with open(f"data/{count}_{categoryName}.html", encoding="utf-8") as file:
		src = file.read()
	soup = BeautifulSoup(src, "lxml")
	alertBlock = soup.find(class_ = "uk-alert-danger")
	if alertBlock is not None:
		continue
	tableHead = soup.find(class_ = "mzr-tc-group-table").find("tr").find_all("th")
		

	

	product = tableHead[0].text
	calories = tableHead[1].text
	proteins = tableHead[2].text
	fats = tableHead[3].text
	carbohydrates = tableHead[4].text
		
	with open(f"data/{count}_{categoryName}.csv", "w", encoding="utf-8") as file:
		writer = csv.writer(file)
		writer.writerow(
			(
				product,
				calories,
				proteins,
				fats,
				carbohydrates
			)
		)
	productsData = soup.find(class_ = "mzr-tc-group-table").find("tbody").find_all("tr")
	productInfo = []
	for item in productsData:
		productsTds = item.find_all("td")
		title = productsTds[0].find("a").text
		calories = productsTds[1].text
		proteins = productsTds[2].text
		fats = productsTds[3].text
		carbohydrates = productsTds[4].text

		productInfo.append(
			{
				"Title": title,
				"Calories": calories,
				"Proteins": proteins,
				"Fats": fats,
				"Carbonhydrates": carbohydrates
			}
		)

		with open(f"data/{count}_{categoryName}.csv", "a", encoding="utf-8") as file:
			writer = csv.writer(file)
			writer.writerow(
				(
					title,
					calories,
					proteins,
					fats,
					carbohydrates
				)
			)
	with open(f"data/{count}_{categoryName}.json", "a", encoding="utf-8") as file:
		json.dump(productInfo, file, indent=4, ensure_ascii=False)
	count += 1
	print(f"# Iteration {count}. {categoryName} written...")
	iterationCount -= 1
	print(f"Iterations left:{iterationCount}")