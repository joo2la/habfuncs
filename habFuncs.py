import requests
from bs4 import BeautifulSoup
#Эта библиотека разрабатывается для игры Habland (hablandhotel.ru) при поддержке Fantik`а.
#Мы не стараемся создать "Жёсткие" функции а просто хотим упростить игру :3


#----------------------------------------------------------НАЗВАНИЕ ФУНКЦИЙ----------------------------------------------------------
# getOnline() -  Выводит текущий онлайн Хаблэнда в формате int(целое число)
# getNicknameByProfile(profile) - Выводит никнейм игрока по профилю в формате str(строковый)
# getStatusByProfile(profile) - Выводит Статус по профилю в формате str(строковый) (онлайн или оффлайн)
# getRegistrationDateByProfile(profile) - Выводит дату регистрации по профилю в формате str(строковый)
# getLasLoginByProfile(profile) - Выводит последнюю дату входа по профилю в формате str(строковый)
# getFriendListByProfile(profile) - Выводит список друзей по профилю в формате list
# getGroupListByProfile(profile) - Выводит список созданных групп по профилю в формате list
# getLastRoomByProfile(profile) - Выводит последние созданные комнаты по профилю в формате list, выводятся id комнат
# getProfileInfo(profile) - Выводит всю информацию о игроке(всё что выше связанное с профилем)
# ----ФУНКЦИИ ТРЕБУЮЩИЕ ЛОГИНА И ПАРОЛЯ----
# getSession(login, password) - Выводит необходимые для дальнейших работ данные(сессию). Принимает логин и пароль
# getOnlineFriendsLink(session) - Выводит list ссылок на друзей. Принимает выход из getSession()
# getMoney(session) - Выводит текущее количество монет в формате int(целое число). Принимает выход из getSession()
# getDucket(session) - Выводит текущее количество дакетов в формате int(целое число). Принимает выход из getSession()
# enterInRoom(session, id) - Перемещает вас(если вы онлайн) в комнату с ID. Принимает выход из getSession() и id Комнаты.

def getOnline() -> int:
	return int(requests.get("https://hablandhotel.ru/api/online").text)

def getNicknameByProfile(profile : str) -> str:
	return profile.replace("https://hablandhotel.ru/profile/", "")

def getStatusByProfile(profile : str) -> str:
	resp = requests.get(profile)
	soup = BeautifulSoup(resp.text, "lxml")
	return soup.find("div", {"class":"details-container status"}).text.replace("Сейчас ", "")

def getRegistrationDateByProfile(profile:str) -> str:
	resp = requests.get(profile)
	soup = BeautifulSoup(resp.text, "lxml")
	return soup.find("div", {"class":"details-container register"}).text.replace("Хаблэнд c ", "")

def getLasLoginByProfile(profile:str) -> str:
	resp = requests.get(profile)
	soup = BeautifulSoup(resp.text, "lxml")
	return soup.find("div", {"class":"details-container last_login"}).text.replace("Последний визит ", "")

def getFriendListByProfile(profile:str) -> list:
	friend_list = []
	resp = requests.get(profile)
	soup = BeautifulSoup(resp.text, 'lxml')
	article = soup.find("article", {"data-section":"friends"})
	soup = BeautifulSoup(str(article), 'lxml')
	links = soup.find_all("a", {"class":"item-container"})
	for item in links:
		link = item.get("href")
		friend_list.append(f"hablandhotel.ru{link}")
	return friend_list

def getGroupListByProfile(profile:str) -> list:
	group_list = []
	resp = requests.get(profile)
	soup = BeautifulSoup(resp.text, 'lxml')
	article = soup.find("article", {"data-section":"groups"})
	soup = BeautifulSoup(str(article), 'lxml')
	links = soup.find_all("a", {"class":"item-container"})
	for item in links:
		soup = BeautifulSoup(str(item), 'lxml')
		group_list.append(soup.find("div", {"class":"item-name"}).text)
	return group_list

def getLastRoomByProfile(profile:str) -> list:
	rooms = []
	resp = requests.get(profile)
	soup = BeautifulSoup(resp.text, 'lxml')
	article = soup.find("article", {"data-section":"rooms"})
	soup = BeautifulSoup(str(article), 'lxml')
	links = soup.find_all("a", {"class":"item-container"})
	for item in links:
		link = item.get("href")
		rooms.append(f"hablandhotel.ru{link}".replace("hablandhotel.ru/hotel?room=", ""))
	return rooms

def getProfileInfo(profile : str) -> dict:
	info = {
		"nickname" : getNicknameByProfile(profile),
		"status" : getStatusByProfile(profile),
		"registratin" : getRegistrationDateByProfile(profile),
		"last_login" : getLasLoginByProfile(profile),
		"friend_list" : getFriendListByProfile(profile),
		"group_list" : getGroupListByProfile(profile),
		"last_rooms" : getLastRoomByProfile(profile)
	}
	return info

def getSession(login:str, password:str):
	ses = requests.Session()
	payload = {
		"username":login,
		"password":password
	}
	ses.post("https://hablandhotel.ru/auth/login/request", data = payload)
	return ses

def enterInRoom(session, roomId:int) -> bool:
	try:
		resp = session.get(f"https://hablandhotel.ru/api/room/{roomId}").json()
	except:
		return False
	if resp["status"] == "error":
		return False
	return True

def getOnlineFriendsLink(session) -> list:
	resp = session.get("https://hablandhotel.ru/home")
	soup = BeautifulSoup(resp.text, 'lxml')
	friend_list = []
	for a in soup.find_all("div", {'class':'friends-container'}):
		temp = BeautifulSoup(str(a), "lxml")
		try:
			friend_list.append(f"https://hablandhotel.ru{temp.find('a').get('href')}")
		except:
			pass
	return friend_list

def getMoney(session) -> int:
	resp = session.get("https://hablandhotel.ru/home")
	soup = BeautifulSoup(resp.text, 'lxml')
	return int(soup.find("div", {"style":"color: #E2AE1D;"}).text)

def getDucket(session) -> int:
	resp = session.get("https://hablandhotel.ru/home")
	soup = BeautifulSoup(resp.text, 'lxml')
	return int(soup.find("div", {"style":"color: #BA7CC2;"}).text)

def getPopularRoomId(session) -> list:
	id_list = []
	resp = session.get("https://hablandhotel.ru/home")
	soup = BeautifulSoup(resp.text, 'lxml')
	table = soup.find("table", {"class":"rooms table table-striped"})
	soup = BeautifulSoup(str(table), 'lxml')
	links = soup.find_all("a", {"class":"button"})
	for item in links:
		link = item.get("href")
		link = link.replace("/api/room/", "")
		id_list.append(int(link))
	return id_list