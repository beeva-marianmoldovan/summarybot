from datetime import datetime
from datetime import timedelta
from slackclient import SlackClient
from libs.database import DB


class Newsletter(object):
	def __init__(self, access_token):
		self.access_token = access_token
		self.db = DB()

	def __getchannel(self, id):
		client = SlackClient(self.access_token)
		try:
			response = client.api_call("channels.info", channel=id)

			if response.get("ok"):
				return response.get("channel")
		except Exception as e:
			print(e)

		return None

	def __getuser(self, id):
		client = SlackClient(self.access_token)
		try:
			response = client.api_call("users.info", user=id)

			if response.get("ok"):
				return response.get("user")
		except Exception as e:
			print(e)

		return None

	def __getchannels(self):
		channels = []

		client = SlackClient(self.access_token)
		response = client.api_call("channels.list")
		if response and response.get("ok"):
			for channel in response.get("channels"):
				channels.append({
					"id": channel.get("id"),
					"name": channel.get("name")
				})

		response = client.api_call("groups.list")
		if response and response.get("ok"):
			for group in response.get("groups"):
				channels.append({
					"id": group.get("id"),
					"name": group.get("name")
				})

		return channels or None

	def __getkeywords(self, channels):
		links = []
		for channel in channels:
			links += self.db.getAll("news", "channel_id", channel.get("id"))

		keywords = {}

		for link in links:
			link_keywords = link.get("keywords").split(",")

			for keyword in link_keywords:
				if not keyword in keywords.keys():
					keywords.append(keyword)

		return keywords or None

	def gettopics(self):
		try:
			channels = self.__getchannels()
			if channels:
				return self.__getkeywords(channels)
		except Exception as e:
			print(e)

		return None

	def getrecents(self):
		end = datetime.today() - timedelta(days=datetime.today().weekday())
		start = end - timedelta(days=7)

		try:
			links = []
			news = self.db.getByDate("news", "date", start, end)
			for new in news:
				keywords = new.get("keywords")
				if keywords:
					tags = keywords.split(",")
					if tags:
						new["keywords"] = tags
						new["summary"] = new.get("summary").split("\n\n")
						channel = self.__getchannel(new.get("channel_id"))
						author = self.__getauthor(channel.get("user_id"))

						if channel:
							del channel["channel_id"]
							new["channel"] = {
								"id": channel.get("id"),
								"name": channel.get("name")
							}

						if author:
							del channel["user_id"]
							new["author"] = {
								"id": author.get("id"),
								"name": author.get("profile").get("real_name") or author.get("name")
							}

						links.append(new)
			return links
		except Exception as e:
			print(e)

		return None

	def getlinks(self, topic):
		try:
			links = []
			news = self.db.getAll("news")
			for new in news:
				keywords = new.get("keywords")
				if keywords:
					tags = keywords.split(",")
					if topic in tags:
						new["keywords"] = tags
						new["summary"] = new.get("summary").split("\n\n")
						links.append(new)

			return links or None
		except Exception as e:
			print(e)

		return None