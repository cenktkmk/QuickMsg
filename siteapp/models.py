from django.db import models
from projeApp.settings import *
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
 
from django.utils import timezone
import math
import uuid








class BannedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    banned_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self) -> str:
        return self.user.username



# Profil Sayfasında kayıt etmek ve Kullanıcının kendi verilerini güncelleyebilmesi için Userdan model çeker. 

class SiteUser(models.Model):

    user = models.OneToOneField(User, verbose_name=("User"), on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, default='./avatars/default-avatar.jpg')
    is_moderator = models.BooleanField(default=False)
    is_banned = models.BooleanField(("banlı kullanıcı"), default=False)
    shared_tweets = models.ManyToManyField('Tweet', related_name='shared_by', blank=True)
    bio = models.TextField(blank=True, null=True, max_length=120)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    education = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    



    def __str__(self) -> str:
        return self.user.username
    








    
 # Kullanıcının post paylaşabilmesi için ve diğer kullanıcıların paylaşılan post ile interact a geçebilmesi için gerekli olan model 
 # kendine has bir id oluşturur ve o id ile report edilirse admin dashboarda düşer 
  

class Tweet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True, max_length=120)
    createdAt = models.DateTimeField(("Oluşturulma Tarihi"), default=timezone.now)
    answers = models.PositiveIntegerField(("Toplam Cevaplar"), default=0)
    like = models.IntegerField(default=0)
    image = models.ImageField(upload_to='tweet-image', blank=True, null=True)


    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.createdAt

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "saniye önce"
            
            else:
                return str(seconds) + " saniye önce"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " dakika önce"
            
            else:
                return str(minutes) + " dakika önce"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " saat önce"

            else:
                return str(hours) + " saat önce"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " gün önce"

            else:
                return str(days) + " gün önce"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " ay önce"

            else:
                return str(months) + " ay önce"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " yıl önce"

            else:
                return str(years) + " yıl önce"



    def __str__(self):
        return f"{self.user.username}: {self.content}"
    

# Kullanıcıların Paylaşılan post altına yorum yapabilmesine yarayan model    

# kendine has bir id oluşturur ve o id ile report edilirse admin dashboarda düşer 
    
class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments', default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True, max_length=60)
    createdAt = models.DateTimeField(("Oluşturulma Tarihi"), default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    def __str__(self) -> str:
        return f"{self.tweet}: {self.user.username}: {self.content}"


# Paylaşılan tweeti reportlamak için 

class ReportedTweet(models.Model):
    reported_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="reported_reports", default=1)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweet_reporters", default=1)
    reason = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)


# Paylaşılan yorumu reportlamak için 
class ReportedComment(models.Model):
    reported_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reported_reports", default=1)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_reporters", default=1)
    reason = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)


class LikePost(models.Model):
    
    post_id=models.CharField(max_length=500, default=1)
    username=models.CharField(max_length=100, default=1)



    def _str_(self):
        return self.username
    



