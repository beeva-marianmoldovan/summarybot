from datetime import datetime
from datetime import timedelta
from libs.database import DB
from slackclient import SlackClient

db = DB()

class Newsletter(object):
	def __init__(self, access_token):
		self.access_token = access_token

	def gettopics(self):
		try:
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

			links = []
			for channel in channels:
				links += db.getAll("news", "channel_id", channel.get("id"))

			keywords = []
			start = datetime.now() - timedelta(days=datetime.now().weekday())
			for link in links:
				if link.get("date") <= start:
					keywords += link.get("keywords").split(",")

			print(keywords)
			return channels
		except Exception as e:
			print(e)

		return None

	def getlinks(user, channel_id):
		try:
			news = db.getAll("news", "channel_id", channel_id)
			for new in news:
				new["keywords"] = new.get("keywords").split(",")

			return news
		except Exception as e:
			print(e)

		return None