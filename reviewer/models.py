from django.db import models

# the reviewer should contain models, which simulate study-cards
# the cards have a Question/Answer field
# Progress stores a value for progress
# or how often it has been studied and a timestamp of the last time studied
# and the next time to study for the specific user

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import signals



# for eventual changes to User
class User(AbstractUser):
    pass

class Card(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    front = models.TextField()
    back = models.TextField()
    #conection between User, Cards and the specific Progress in one SQL table(?)
    users = models.ManyToManyField(User, through='Progress')

    def __str__(self):
        return self.title




# extends the User Model with the Card Progress
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0, null=True)
    lasttime = models.DateField(blank=True, null=True)
    nexttime = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.user) + str(': ') + str(self.card)


#autocreation of the Progress for every Card if a User is created
#(receives the post.save signal, which activates the function)
def create_progress_new_user(sender, instance, created, **kwargs):
    #"""Create ModelB for every new ModelA."""
    if created:
        for card in Card.objects.all():
            Progress.objects.create(user=instance, card=card)


signals.post_save.connect(create_progress_new_user, sender=User, weak=False,
                          dispatch_uid='models.create_progress_new_user')

#autocreation of Progress for all Users for every new Card
def create_progress_new_card(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            Progress.objects.create(user=user, card=instance)

signals.post_save.connect(create_progress_new_card, sender=Card, weak=False,
                          dispatch_uid='models.create_progress_new_card')







# old try
#class UserProgress(models.Model):
    #card = models.ForeignKey(Card, on_delete=models.CASCADE)
    #user = models.CharField(max_length=50)
    #progress = models.IntegerField(default=0, null=True)
    #lasttime = models.DateField(blank=True, null=True)
    #nexttime = models.DateField(blank=True, null=True)

    #def __str__(self):
        #return self.user
