from django.db import models

# Create your models here.
class Friend(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    invite_code = models.CharField(max_length = 100,blank=True) # 邀請碼
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True, blank=True)
    def __str__(self):
        message = dict()
        message = {
            'uid':self.uid,
            'invite_code':self.invite_code        
        }
        return str(message)

class Friend_data(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    relation_id = models.CharField(max_length = 100,blank=True)
    friend_type = models.IntegerField(blank=True)
    status = models.CharField(max_length = 100,blank=True)
    read = models.BooleanField(blank=True,default=False)
    imread = models.BooleanField(blank=True,default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True, blank=True)
    def __str__(self):
        message = dict()
        message = {
            'uid':self.uid,
            'relation_id':self.relation_id,
            'friend_type':self.friend_type,
            'status':self.status,
            'read':self.read,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(message)