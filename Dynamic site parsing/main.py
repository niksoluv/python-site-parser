import requests
from bs4 import BeautifulSoup
import json
import os

def GetData(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
	}
	projectsDataList = []
	iterationCount = 23

	print(f"Total iterations: #{iterationCount}")

	for item in range(1, 24):

		req = requests.get(url + f"&PAGEN_1={item}&PAGEN_2={item}", headers)

		folderName = f"data/data_{item}"

		if os.path.exists(folderName):
			print("Folder already exists")
		else:
			os.mkdir(folderName)
		
		with open(f"{folderName}/projects_{item}.html", "w", encoding="utf-8") as file:
			file.write(req.text)

		with open(f"{folderName}/projects_{item}.html", "r", encoding="utf-8") as file:
			src = file.read()

		soup = BeautifulSoup(src, "lxml")
		articles = soup.find_all("article", class_ = "ib19")
		
		projectUrls = []
		for item in articles:
			projectUrl = "http://www.edutainme.ru" + item.find("div", class_ = "txtBlock").find("a").get("href")
			projectUrls.append(projectUrl)
		
		for projectUrl in projectUrls:
			req = requests.get(projectUrl, headers)
			projectName = projectUrl.split("/")[-2]

			with open(f"{folderName}/{projectName}.html", "w", encoding="utf-8") as file:
				file.write(req.text)
			with open(f"{folderName}/{projectName}.html", "r", encoding="utf-8") as file:
				src = file.read()
			
			soup = BeautifulSoup(src, "lxml")

			projectData = soup.find("div", class_ = "inside")
			
			try:
				projectLogo = "http://www.edutainme.ru" + projectData.find("div", class_ = "Img logo").find("img").get("src")
			except Exception:
				projectLogo = "None Logo"
			try:
				projectName = "http://www.edutainme.ru" + projectData.find("div", class_ = "txt").find("h1").text
			except Exception:
				projectName = "None name"
			try:
				projectShortDescription = projectData.find("div", class_ = "txt").find("h4", class_="head").text
			except Exception:
				projectShortDescription = "None short description"
			try:
				projectWebsite = projectData.find("div", class_ = "txt").find("p").find("a").get("href")
			except Exception:
				projectWebsite = "None website"
			try:
				projectFullDescription = projectData.find("div", class_="textWrap").find("div", class_="rBlock").find("p").text
			except Exception:
				projectFullDescription = "None full description"

			projectsDataList.append({
				"project name:": projectName,
				"project logo URL:": projectLogo,
				"project short description:": projectShortDescription,
				"project long description:": projectFullDescription.strip(),
				"project website:": projectUrl			
			})
		iterationCount-=1
		print(f"Iteration {item} finished, iterations left: {iterationCount}")
		if iterationCount==0:
			print("Data collection finished")
	
	with open("data/projectsData.json", "a", encoding="utf-8") as file:
		json.dump(projectsDataList, file, indent=4, ensure_ascii=False)

GetData("http://www.edutainme.ru/edindex/ajax.php?params=%7B%22LETTER%22%3Anull%2C%22RESTART%22%3A%22N%22%2C%22CHECK_DATES%22%3Afalse%2C%22arrWHERE%22%3A%5B%22iblock_startaps%22%5D%2C%22arrFILTER%22%3A%5B%22iblock_startaps%22%5D%2C%22startups%22%3A%22Y%22%2C%22SHOW_WHERE%22%3Afalse%2C%22PAGE_RESULT_COUNT%22%3A9%2C%22CACHE_TYPE%22%3A%22A%22%2C%22CACHE_TIME%22%3A0%2C%22TAGS_SORT%22%3A%22NAME%22%2C%22TAGS_PAGE_ELEMENTS%22%3A%22999999999999999999%22%2C%22TAGS_PERIOD%22%3A%22%22%2C%22TAGS_URL_SEARCH%22%3A%22%22%2C%22TAGS_INHERIT%22%3A%22Y%22%2C%22SHOW_RATING%22%3A%22Y%22%2C%22FONT_MAX%22%3A%2214%22%2C%22FONT_MIN%22%3A%2214%22%2C%22COLOR_NEW%22%3A%22000000%22%2C%22COLOR_OLD%22%3A%22C8C8C8%22%2C%22PERIOD_NEW_TAGS%22%3A%22%22%2C%22DISPLAY_TOP_PAGER%22%3A%22N%22%2C%22DISPLAY_BOTTOM_PAGER%22%3A%22N%22%2C%22SHOW_CHAIN%22%3A%22Y%22%2C%22COLOR_TYPE%22%3A%22Y%22%2C%22WIDTH%22%3A%22100%25%22%2C%22USE_LANGUAGE_GUESS%22%3A%22N%22%2C%22PATH_TO_USER_PROFILE%22%3A%22%23SITE_DIR%23people%5C%2Fuser%5C%2F%23USER_ID%23%5C%2F%22%2C%22SHOW_WHEN%22%3Afalse%2C%22PAGER_TITLE%22%3A%22%5Cu0420%5Cu0435%5Cu0437%5Cu0443%5Cu043b%5Cu044c%5Cu0442%5Cu0430%5Cu0442%5Cu044b+%5Cu043f%5Cu043e%5Cu0438%5Cu0441%5Cu043a%5Cu0430%22%2C%22PAGER_SHOW_ALWAYS%22%3Afalse%2C%22USE_TITLE_RANK%22%3Afalse%2C%22PAGER_TEMPLATE%22%3A%22%22%2C%22DEFAULT_SORT%22%3A%22rank%22%2C%22noTitle%22%3A%22Y%22%7D")