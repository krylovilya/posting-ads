import json

from channels.generic.websocket import WebsocketConsumer

from apps.main.models import Ad


class ChatConsumer(WebsocketConsumer):
    """Consumer для чата."""

    groups = ('chat',)

    def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return
        ad_qs = Ad.objects.filter(title__iexact=text_data)
        if ad_qs:
            ad = ad_qs[0]
            self.send(text_data=json.dumps({
                'id': ad.id,
                'title': ad.title,
            }))
        else:
            self.send(text_data='Not found')
