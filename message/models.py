from django.db import models


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'messages'
