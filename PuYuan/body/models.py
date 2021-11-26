from django.db import models

# Create your models here.
class Blood_pressure(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    systolic = models.FloatField(max_length=3, default=0, null=True)
    diastolic = models.FloatField(max_length=3, default=0, null=True)
    pulse = models.CharField(max_length =3, default=0, null=True)
    recorded_at= models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True, blank=True)
    def __str__(self):
        message = dict()
        message = {
            'uid':self.uid,
            'systolic':self.systolic,
            'diastolic':self.diastolic,
            'pulse':self.pulse,
            'recorded_at':self.recorded_at,
            'created_at':self.created_at,
            'date':self.date
        }
        return str(message)
class Weight(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    weight = models.FloatField(max_length=10, default=0, null=True)
    body_fat = models.FloatField(max_length=10, default=0, null=True)
    bmi = models.FloatField(max_length=10, default=0, blank=True)
    recorded_at= models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True, blank=True)
    def __str__(self):
        message = dict()
        message = {
            'uid':self.uid,
            'weight':self.weight,
            'body_fat':self.body_fat,
            'bmi':self.bmi,
            'recorded_at':self.recorded_at,
            'created_at':self.created_at,
            'date':self.date
        }
        return str(message)
class Blood_sugar(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    sugar = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=0)# 血糖
    timeperiod = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=0) # 時段
    recorded_at= models.DateTimeField(auto_now=False, auto_now_add=False, blank=True) # 上傳時間
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True, blank=True)
    def __str__(self):
        message = dict()
        message = {
            'uid':self.uid,
            'sugar':self.sugar,
            'timeperiod':self.timeperiod,
            'recorded_at':self.recorded_at,
            'created_at':self.created_at,
            'date':self.date
        }
        return str(message)
class Diary_diet(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    description = models.CharField(max_length=5, blank=True, null=True, default=0)
    meal = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=0)
    tag = models.CharField(max_length = 100,blank=True)
    image = models.ImageField(upload_to = 'diet/diet_%Y-%m-%D_%H:%M:%S',blank=True)
    image_count = models.IntegerField(blank=True)
    lat = models.FloatField(max_length = 100,blank=True)
    lng = models.FloatField(max_length = 100,blank=True)
    recorded_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True, blank=True)
    def __str__(self):
        message = dict()
        message = {
            'uid':self.uid,
            'description':self.description,
            'meal':self.meal,
            'tag':self.tag,
            'image':self.image,
            'image_count':self.image_count,
            'lat':self.lat,
            'lng':self.lng,
            'recorded_at':self.recorded_at
        }
        return str(message)

class UserCare(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    member_id = models.CharField(max_length = 100,blank=True)
    reply_id = models.CharField(max_length = 100,blank=True)
    message = models.CharField(max_length = 100,blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True, blank=True)
    def __str__(self):
        message = dict()
        message = {
            'uid':self.uid,
            'member_id':self.member_id,
            'reply_id':self.reply_id,
            'message':self.message,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
            'date':self.date
        }
        return str(message)