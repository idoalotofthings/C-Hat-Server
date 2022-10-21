import string, random
from django.db import models

class ChatUser(models.Model):
    client_id = models.TextField(primary_key=True)
    mail_id = models.TextField()
    username = models.TextField()
    password = models.TextField()

    def __str__(self):
        return f"Client {self.username}, {self.client_id}"

    def _generate_client_id():
        client_id = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k = 5))
        while ChatUser.objects.filter(client_id=client_id).exists():
            client_id = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k = 7))
        return client_id

    generate_client_id = staticmethod(_generate_client_id)