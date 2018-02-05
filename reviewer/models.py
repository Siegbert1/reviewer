

# the reviewer should contain models, which simulate study-cards
# the cards have a Question/Answer field
# Progress stores a value for progress
# or how often it has been studied and a timestamp of the last time studied
# and the next time to study for the specific user

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User
from django.db.models import signals
from django.dispatch import receiver
from django.contrib import admin


# for eventual changes to User
class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=50)
    STRAF = 'SR'
    OEFF = 'OR'
    ZIVR = 'ZR'
    AREA_CHOICES = (
        (STRAF, 'Strafrecht'),
        (OEFF, 'Oeffentliches Recht'),
        (ZIVR, 'Zivilrecht'),
    )
    area = models.CharField(
        max_length=2,
        choices=AREA_CHOICES,
        default=STRAF,
    )
    containing_cards = models.IntegerField(default=1, blank=True, null=True)
    def __str__(self):
        return self.name

class Card(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    front = models.TextField()
    back = models.TextField()
    explanation = models.TextField(blank=True, null=True)
    #conection between User, Cards and the specific Progress in one SQL table(?)
    users = models.ManyToManyField(User, through='Progress')

    def __str__(self):
        return self.title





# extends the User Model with the Card Progress
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0, null=True)
    lasttime = models.DateTimeField(auto_now=True, blank=True, null=True)
    nexttime = models.DateTimeField(default=timezone.now, blank=True, null=True)

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
# auto-updating the card_count in category
        cat = Category.objects.get(name=instance.category)
        cat.containing_cards = len(Card.objects.filter(category=cat))
        cat.save()

signals.post_save.connect(create_progress_new_card, sender=Card, weak=False,
                          dispatch_uid='models.create_progress_new_card')





class Case_ZR(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField()
    explanation = models.TextField()
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    # score?
    solution = models.CharField(max_length=150, blank=True, null=True)
# Vertraglich
# Kaufvertrag
    kv = models.BooleanField(default=False)
    kp = models.BooleanField(default=False)
    mangel = models.BooleanField(default=False)
    kp2 = models.BooleanField(default=False)
    gefahruebergang = models.BooleanField(default=False)
    kp3 = models.BooleanField(default=False)
#Werkvertrag
    wv = models.BooleanField(default=False)
    wp = models.BooleanField(default=False)
    wvmangel = models.BooleanField(default=False)
    wp2 = models.BooleanField(default=False)
    abnahme = models.BooleanField(default=False)
    wp3 = models.BooleanField(default=False)
#Dienstvertrag
    dv = models.BooleanField(default=False)
    dp = models.BooleanField(default=False)
    
# Quasivertraglich
# CiC
    cic = models.BooleanField(default=False)
    cp = models.BooleanField(default=False)
    cicpv = models.BooleanField(default=False)
    cp2 = models.BooleanField(default=False)
    cicvm = models.BooleanField(default=False)
    cp3 = models.BooleanField(default=False)

    def __str__(self):
        return self.title
