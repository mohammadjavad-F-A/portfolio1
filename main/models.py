from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels
from datetime import datetime
class create_projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField()
    project_name = models.CharField()
    project_description = models.CharField()
    langu = models.CharField()
    day = models.IntegerField(null=True)
    price = models.CharField()
    date2 = models.DateField(default=datetime.now())
    created_date = jmodels.jDateField(default=datetime.now)
    created_date2 = jmodels.jDateTimeField(default=datetime.now)

    def __str__(self):
        return self.project_name + self.user.username

class msgs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')

    confirm_pro = models.IntegerField()
    confirm_msg = models.CharField()
    description = models.CharField()

    is_read = models.BooleanField(default=False)
    date_1 = jmodels.jDateField(default=datetime.now)
    date_2 = jmodels.jDateTimeField(default=datetime.now)
    date_3 = models.DateTimeField(default=datetime.now)

    reply = models.CharField()
    read_date1 = jmodels.jDateTimeField(default=datetime.now)
    read_date2 = jmodels.jDateField(default=datetime.now)
    def __str__(self):
        return f"{self.confirm_pro} + {str(self.user.username)}"

class basics(models.Model):
    description_1 = models.CharField()
    description_2 = models.CharField()
    description_3 = models.CharField()
    description_4 = models.CharField()

    image_main = models.ImageField(upload_to='img')
    image_1 = models.ImageField(upload_to='img')
    image_2 = models.ImageField(upload_to='img')
    image_3 = models.ImageField(upload_to='img')
    image_4 = models.ImageField(upload_to='img')
    image_5 = models.ImageField(upload_to='img')
    image_6 = models.ImageField(upload_to='img')


class front_end(models.Model):
    title = models.CharField()
    darsad = models.IntegerField()

    def __str__(self):
        return self.title

class back_end(models.Model):
    title = models.CharField()
    darsad = models.IntegerField()
    def __str__(self):
        return self.title

class realtors(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    title_0 = models.CharField()
    title_1 = models.CharField()
    skills = models.CharField()
    email = models.CharField()
    instagram = models.CharField()
    telegram = models.CharField()
    image = models.ImageField(upload_to='img')
    age = models.IntegerField()

    def __str__(self):
        return self.first_name

class project_sample(models.Model):
    image_main = models.ImageField(upload_to='img')
    image_1 = models.ImageField(upload_to='img')
    image_2 = models.ImageField(upload_to='img')
    image_3 = models.ImageField(upload_to='img')
    image_4 = models.ImageField(upload_to='img')
    image_5 = models.ImageField(upload_to='img')
    created_by = models.CharField()
    title_main_1 = models.CharField()
    title_main_2 = models.CharField()
    title_1 = models.CharField()
    title_2 = models.CharField()
    title_3 = models.CharField()
    link_to = models.CharField()

    def __str__(self):
        return self.title_main_1

class project_details(models.Model):
    for_project = models.ForeignKey(project_sample, on_delete=models.CASCADE)
    title = models.CharField()

    def __str__(self):
        return self.for_project.title_main_1


class contacts(models.Model):
    title = models.CharField()

    def __str__(self):
        return self.title

class aboutus(models.Model):
    title = models.CharField()
    image = models.ImageField(upload_to='img')

    def __str__(self):
        return self.title

class contact_s(models.Model):
    name = models.CharField()
    email = models.CharField()
    contact = models.CharField()

    def __str__(self):
        return self.name

class img_create(models.Model):
    img = models.ImageField(upload_to='img')

    def __str__(self):
        return self.img.url
