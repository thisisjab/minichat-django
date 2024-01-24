import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "message": "You are now connected to the chat server.",
                }
            )
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(
            text_data=json.dumps(
                {
                    "type": "chat",
                    "message": f"{self.scope['user'].username}: {message}",
                }
            )
        )
