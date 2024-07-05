import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message,Status
from django.core.files.base import ContentFile
import urllib.parse

class Chat_consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']

        query_string = self.scope['query_string'].decode('utf-8')
        query_params = urllib.parse.parse_qs(query_string)

        self.username = query_params.get('username', [None])[0]
        self.status = query_params.get('status', [None])[0]

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.status_connect()
        grp_status = await self.status_user()

        previous_messages = await self.get_previous_messages()
        await self.send(text_data=json.dumps({
            'type': 'previous_messages',
            'messages': previous_messages,
            'status':grp_status
        }))

    async def disconnect(self, close_code):
        await self.status_disconnect()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    @database_sync_to_async
    def status_connect(self):
        user_status = Status.objects.filter(username=self.username)
        if len(user_status) > 0:
            for var in user_status:
                var.status = True
                var.save()
        else:
            Status.objects.create(username=self.username, status=True)

    @database_sync_to_async
    def status_disconnect(self):
        user_status = Status.objects.filter(username=self.username)
        for i in user_status:
            i.status = False
            i.save()

    @database_sync_to_async
    def save_message(self,messge=None,byte_data=None):
        Admin = False
        messg = Message.objects.filter(room_name=self.room_group_name, username=self.username)
        for i in messg:
            if i.admin:
                Admin = True
                break
        if byte_data:
            if Admin:
                img = Message(username=self.username, room_name=self.room_group_name, message="", admin=True,
                              status=self.status, request_grp="")
            else:
                img = Message(username=self.username, room_name=self.room_group_name, message="", admin=False,
                              status=self.status, request_grp="")
            img_url = f'{self.username}_{self.room_group_name}.jpg'
            img.image.save(img_url, ContentFile(byte_data))
            img.save()
            img_str = str(img.image.url)
            return img_str
        elif messge:
            if Admin:
                Message.objects.create(room_name=self.room_group_name, username=self.username, message=messge,
                                       admin=True, status=self.status, request_grp="")
            else:
                Message.objects.create(room_name=self.room_group_name, username=self.username, message=messge,
                                       admin=True, status=self.status, request_grp="")
            return


    @database_sync_to_async
    def get_previous_messages(self):
        msg = Message.objects.filter(room_name=self.room_group_name)
        list1 = []
        for m in msg:
            dict1 = {}
            dict1['username'] = m.username
            if str(m.message) != "Hii":
                dict1['message'] = m.message
            if m.image:
                dict1['image'] = str(m.image.url)
            list1.append(dict1)
        return list1

    @database_sync_to_async
    def status_user(self):
        user_status = Status.objects.all()
        grp = Message.objects.filter(room_name=self.room_group_name)
        users = []
        for user in grp:
            if str(user.username) != str(self.username):
                users.append(str(user.username))
        users_list = list(set(users))
        dict_status = {}
        if len(users_list) == 1:
            for i in user_status:
                for j in users_list:
                    if str(i.username) == str(j):
                        if i.status == True:
                            dict_status[j] = "Online"
                        else:
                            dict_status[j] = "Offline"
        return dict_status


    async def receive(self, text_data=None, bytes_data=None):
        grp_status = await self.status_user()
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            await self.save_message(message,bytes_data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat_messages',
                    'message':message,
                    'username':self.username,
                    'status': grp_status
                }
            )
        if bytes_data:
            image_url = await self.save_message(text_data,bytes_data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'image_file',
                    'url': image_url,
                    'username': self.username,
                    'status': grp_status
                }
            )

    async def chat_messages(self,event):
        message = event['message']
        username = event['username']
        status = event['status']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'status': status
        }))
    async def image_file(self,event):
        image_url = event['url']
        user = event['username']
        status = event['status']
        await self.send(text_data=json.dumps({
            'type': 'image',
            'username': user,
            'url': image_url,
            'status': status
        }))


