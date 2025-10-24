
from django.db import models

class profile_user(models.Model):
    user_name = models.CharField()
    user_id = models.IntegerField()
    img = models.FileField(upload_to="profile_pics/", default="assets/img/img_avatar.jpg")

    def __str__(self):
        return str(self.user_name)

class users_pass(models.Model):
    user = models.CharField()
    userid = models.IntegerField()
    password = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return str(self.user)