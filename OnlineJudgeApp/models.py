from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	rating=models.IntegerField(default=1500)
	isRated=models.BooleanField(default=False)
	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Contest(models.Model):
	contest_id=models.AutoField(primary_key=True)
	start_time=models.DateTimeField()
	duration=models.DurationField()
	ratingUpdated=models.BooleanField(default=False)
	def __str__(self):
		return str(self.contest_id)

class Blog(models.Model):
	blog_id=models.AutoField(primary_key=True)
	title=models.CharField(max_length=100)
	content=models.TextField()
	timestamp=models.DateTimeField()
	isImportant=models.BooleanField(default=False)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	def __str__(self):
		return self.title

class Comment(models.Model):
	comment_id=models.AutoField(primary_key=True)
	content=models.TextField()
	timestamp=models.DateTimeField()
	blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
	def __str__(self):
		return self.content

class Problem(models.Model):
	prob_id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=100)
	content=models.TextField()
	time_limit=models.IntegerField()
	mem_limit=models.IntegerField()
	addedToPractice=models.BooleanField(default=False)
	user_solved=models.IntegerField(default=0)
	checker=models.TextField()
	setter=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return self.name


class Submission(models.Model):
	sub_id=models.AutoField(primary_key=True)
	timestamp=models.DateTimeField()
	verdict=models.CharField(max_length=3)
	prob_id=models.ForeignKey(Problem,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)


class Test(models.Model):
	test_id=models.AutoField(primary_key=True)
	data=models.BinaryField()
	problem=models.ForeignKey(Problem,on_delete=models.CASCADE)

class Tag(models.Model):
	tag=models.CharField(primary_key=True,max_length=100)
	def __str__(self):
		return self.tag

class ProbTag(models.Model):
	class Meta:
		unique_together=(('prob','tag'))
	prob=models.ForeignKey(Problem,on_delete=models.CASCADE)
	tag=models.ForeignKey(Tag,on_delete=models.CASCADE)

class ProbContest(models.Model):
	problem=models.OneToOneField(Problem,on_delete=models.CASCADE,primary_key=True)
	contest=models.ForeignKey(Contest,on_delete=models.CASCADE)
	idx=models.CharField(max_length=1)

class regnConfirm(models.Model):
	regn_id=models.AutoField(primary_key=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	hashval=models.TextField()