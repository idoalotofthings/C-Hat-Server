import random
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
from chat.models import ChatUser
from django.core.mail import send_mail
import json

class ChatServiceConsumer(AsyncJsonWebsocketConsumer):

    is_authorised = False
    json_data = None
    start_millis = None

    async def connect(self):
        await self.accept()
        
    async def receive(self, text_data):
        
        if self.is_authorised == False:
            await self.authorise(text_data)
        else:
            try:
                json_data = json.loads(text_data)
                await self.channel_layer.group_send(
                   json_data["rcid"],
                   {
                      "type":  "chat.message",
                      "rcid" : json_data["rcid"],
                      "message": json_data["message"],
                      "author": json_data["author"],
                      "time": json_data["time"]
                   }
                )
            except Exception as e:
                print(e)
            
    async def disconnect(self, code):
        print(code)


    async def authorise(self, data):
        try:
            json_data = json.loads(data)

            if await self.query(json_data["mail_id"]) == False:
                await self.send_json({
                    "event": "auth",
                    "status": "error",
                    "message": "User doesn't exist on this server"
                })
                await self.close(3001)

            if json_data["password"] == await self.get_user_password(await self.get_user(json_data["mail_id"])):
                self.is_authorised = True
                await self.channel_layer.group_add(await self.get_user_id(json_data["mail_id"]), self.channel_name)
                await self.send_json({
                    "event": "auth",
                    "status": "done",
                    "client_id": str(await self.get_user_id(json_data["mail_id"]))
                })
            else:
                await self.send_json({
                    "event": "auth",
                    "status": "error",
                    "message": "Incorrect Password"
                })
                await self.close(3001)
        except  Exception as e:
            print("Retrying, ", e)


    async def chat_message(self, event):
        try:
            await self.send_json({
                "event": "message"
                "message": event["message"],
                "author": event["author"],
                "time": event["time"],
                "rcid": event["rcid"]
            })
        except Exception as e:
            print("Error sending the message\n", e)

    @sync_to_async
    def query(self, mail_id):
        return ChatUser.objects.filter(mail_id=mail_id).exists()
        
    @sync_to_async
    def get_user_password(self, pk):
        return ChatUser.objects.get(pk=pk).password

    @sync_to_async
    def get_user(self, mail_id) -> ChatUser:
        return ChatUser.objects.get(mail_id=mail_id)

    @sync_to_async
    def get_user_id(self, mail_id):
        return ChatUser.objects.get(mail_id=mail_id).client_id

class RegisterUserConsumer(AsyncJsonWebsocketConsumer):

    _verification_code = None
    _username = None
    _password = None
    _mail_id = None

    async def connect(self):
        await self.accept()
    
    async def receive(self, text_data):
        json_data = json.loads(text_data)

        if json_data["event"] == "register":
            try:
                if await self.query(json_data["mail_id"]) == False:
                    self._username = json_data["username"]
                    self._password = json_data["password"]
                    self._mail_id = json_data["mail_id"]
                    code = random.randrange(100000, 999999)
                    self._verification_code = code
                    message = f'Hey {json_data["username"]}, thanks for joining C-Hat.\n\n Your verification code is {code}.\n Enter this code in your C-Hat client to start chatting'
                    send_mail(f'Verify your email', message, None, [json_data["mail_id"]], fail_silently=False)

                else:
                    await self.send_json({
                        "event": "info",
                        "message": "Mail ID already exists"
                    })

                    await self.close()
                
            except Exception as e:
                print("Can't register user: ", e)

        elif json_data["event"] == "confirmation":
            print(json_data["code"] == str(self._verification_code))
            if json_data["code"] == str(self._verification_code):
                new_user = ChatUser(
                    client_id = await self.generate_client_id(),
                    username = self._username,
                    password = self._password,
                    mail_id = self._mail_id
                )

                await sync_to_async(new_user.save)()
                await self.send_json({
                    "event": "confirmation",
                    "status": "done"
                })

            else:
                await self.send_json({
                    "event": "confirmation",
                    "status": "error"
                })

        else:
            await self.close(3001)

    @sync_to_async
    def query(self, mail_id):
        return ChatUser.objects.filter(mail_id=mail_id).exists()      

    @sync_to_async
    def generate_client_id(self):
        return ChatUser.generate_client_id()

 
