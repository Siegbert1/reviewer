

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
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, blank=True, null=True)
    # score?
    solution = models.CharField(max_length=150, blank=True, null=True)



# Vertraglich
    # Vertragsschluss
    v = models.BooleanField(default=False)
    p = models.BooleanField(default=False)
    # Willenserklärung
        # Angebot und Annahme, nur wenn (P)
            #Erklärung
        willp = models.BooleanField(default=False)
            #Zugang
        willp2 = models.BooleanField(default=False)
            #Erklärung
        willp3 = models.BooleanField(default=False)
            #Zugang
        willp4 = models.BooleanField(default=False)
        #Vertreter §164ff
        vertew = models.BooleanField(default=False)
        vertp = models.BooleanField(default=False)
        vertifn = models.BooleanField(default=False)
        vertp2 = models.BooleanField(default=False)
        vertmitvm = models.BooleanField(default=False)
        vertp3 = models.BooleanField(default=False)
    #rechtshindernde Einwendungen
        #105, 108
        gup = models.BooleanField(default=False)
        guausnahme = models.BooleanField(default=False)

        #116, 117, 118
        ernst = models.BooleanField(default=False)
        ernstp = models.BooleanField(default=False)
        #125
        formnichtigkeit = models.BooleanField(default=False)
        formp = models.BooleanField(default=False)
        formheilung = models.BooleanField(default=False)
        formp2 = models.BooleanField(default=False)
        #134, 135
        gesetzlverbot = models.BooleanField(default=False)
        gesetzlverbotp = models.BooleanField(default=False)
        #138
        sittenwidrig = models.BooleanField(default=False)
        sittenp = models.BooleanField(default=False)
        #142
        anfgrund = models.BooleanField(default=False)
        anfp = models.BooleanField(default=False)
        anferkl = models.BooleanField(default=False)
        anfp2 = models.BooleanField(default=False)
        anffrist = models.BooleanField(default=False)
        anfp3 = models.BooleanField(default=False)
        #


    # Kaufvertrag §433

    #Gewährleistungsrecht oder Schuldrecht AT
    kmangel = models.BooleanField(default=False)
    kp = models.BooleanField(default=False)
    kgefahrue = models.BooleanField(default=False)
    kp2 = models.BooleanField(default=False)
    #Nacherfüllung
        #Nachbesserung
    ne1 = models.BooleanField(default=False)
    nep = models.BooleanField(default=False)
        #Nachlieferung
    ne2 = models.BooleanField(default=False)
    ne2p = models.BooleanField(default=False)

    #Darlehen §488

    #Schenkung §516
        #form heilung

    #Miete §535
    mv = models.BooleanField(default=False)
    mp = models.BooleanField(default=False)
    #SchE Mieter
    #Kündigung
    #

    #Leihe §598
    lv = models.BooleanField(default=False)
    lp = models.BooleanField(default=False)

    #Dienstvertrag §611
    dv = models.BooleanField(default=False)
    dp = models.BooleanField(default=False)

    #Werkvertrag §631
    wv = models.BooleanField(default=False)
    wp = models.BooleanField(default=False)
    wvmangel = models.BooleanField(default=False)
    wp2 = models.BooleanField(default=False)
    abnahme = models.BooleanField(default=False)
    wp3 = models.BooleanField(default=False)


    #Reisevertrag §651a


    #Auftrag §662

    #Geschäftsbesorgung §675

    #Verwahrung §688

    #Bürgschaft §765

    #SchE §280
    ksepflichtverletzung = models.BooleanField(default=False)
    ksep = models.BooleanField(default=False)
    # iVm. 281 frist
    kse1 = models.BooleanField(default=False)
    ksep2 = models.BooleanField(default=False)
    #iVm. 282 nebenpflichtverletzung
    kse2 = models.BooleanField(default=False)
    ksep3 = models.BooleanField(default=False)
    #iVm. §283  unmöglichkeit
    kse3 = models.BooleanField(default=False)
    ksep4 = models.BooleanField(default=False)
    #iVm. §311a anf. Unm
    kse4 = models.BooleanField(default=False)
    ksep5 = models.BooleanField(default=False)

    ksevertr = models.BooleanField(default=False)
    ksep6 = models.BooleanField(default=False)
    # Ausschluss des SchE
    kseausschl = models.BooleanField(default=False)
    ksep7 = models.BooleanField(default=False)

    #Rücktritt §346
    #grund
    krgrundvertragl = models.BooleanField(default=False)
    krp = models.BooleanField(default=False)

    # §323 I
    #gegenseitiger vertrag
    krgegens = models.BooleanField(default=False)
    krp2 = models.BooleanField(default=False)
    #nicht-/schlechtleistung(Mangel) = pflichtverletzung
    krleistung = models.BooleanField(default=False)
    krp3 = models.BooleanField(default=False)
    #fällig/durchsetzb Anspruch
    kranspruch = models.BooleanField(default=False)
    krp4 = models.BooleanField(default=False)
    #frist/ Entbehrlichkeit
    krfrist = models.BooleanField(default=False)
    krp5 = models.BooleanField(default=False)

    #324
    kr324  = models.BooleanField(default=False)
    krp6 = models.BooleanField(default=False)

    #326 V
    krgegens2 = models.BooleanField(default=False)
    krp7 = models.BooleanField(default=False)
    krunmoegl = models.BooleanField(default=False)
    krp8 = models.BooleanField(default=False)

    # Ausschluss des Rücktritts
    krausschluss = models.BooleanField(default=False)
    krp9 = models.BooleanField(default=False)

    # AGB-Kontrolle §305ff.

# Quasivertraglich
# CiC
    cic = models.BooleanField(default=False)
    cp = models.BooleanField(default=False)
    cicpv = models.BooleanField(default=False)
    cp2 = models.BooleanField(default=False)
    cicvm = models.BooleanField(default=False)
    cp3 = models.BooleanField(default=False)

# Dinglich
    #Herausgabe
    #§985
    besitzer = models.BooleanField(default=False)
    ebvp = models.BooleanField(default=False)
    eigentuemer = models.BooleanField(default=False)
        # 1006

        #929 I
    deinigung = models.BooleanField(default=False)
    dingp = models.BooleanField(default=False)
    duebergabe = models.BooleanField(default=False)
    dingp2 = models.BooleanField(default=False)
            #929 S.2ff
    dberechtigung = models.BooleanField(default=False)
    dingp3 = models.BooleanField(default=False)
        # §185

        # §§932 I ff
    dverkehrsg = models.BooleanField(default=False)

    #guter glaube bei erwerb
    dgg = models.BooleanField(default=False)

    dabhanden = models.BooleanField(default=False)


    ebvp2 = models.BooleanField(default=False)
    besitzrecht = models.BooleanField(default=False)
    ebvp3 = models.BooleanField(default=False)

    # Schadensersatz
        #§292

    # Nutzungsersatz
    # Aufwendungsersatz
        #§292

#Deliktisch
    #§823 I

    #§823 II iVm. Norm X

#Bereicherungsrechtlich
    #§812 I 1 1.Alt, 2 1./2.Alt
    etwaserl = models.BooleanField(default=False)
    berp = models.BooleanField(default=False)
    durchl = models.BooleanField(default=False)
    berp2 = models.BooleanField(default=False)
    ohnerg = models.BooleanField(default=False)
    berp3 = models.BooleanField(default=False)


    #§816 S.1

    #§816 S.2 1.Alt

    #§816 S.2 2.Alt

    #§812 I 1 2.Alt
    etwaserl2 = models.BooleanField(default=False)

    sonstigew = models.BooleanField(default=False)

    aufkosten = models.BooleanField(default=False)

    ohnerg2 = models.BooleanField(default=False)
    #§822

#Einwendungen

#rechtsvernichtende Einwendungen
    # §275
    unmoegl = models.BooleanField(default=False)
    unmoeglp = models.BooleanField(default=False)
    # §326 I
    unmoegl2 = models.BooleanField(default=False)
    unmoeglp2 = models.BooleanField(default=False)
    gegennorm = models.BooleanField(default=False)
    gegennormp = models.BooleanField(default=False)
    #Erfüllung §362
    erfuellung = models.BooleanField(default=False)
    erfp = models.BooleanField(default=False)
    #Aufrechnung §389
    aufrechnung = models.BooleanField(default=False)
    aufrp = models.BooleanField(default=False)
    #Abtretung §398
    abtretung = models.BooleanField(default=False)
    abtrp = models.BooleanField(default=False)
# Einreden, peremptorisch, dilatorisch
    #214, 218
    verjaehrung = models.BooleanField(default=False)
    verjp = models.BooleanField(default=False)
    #242
    treuglaube = models.BooleanField(default=False)
    treuglaubep = models.BooleanField(default=False)

# ZPO ?

    def __str__(self):
        return self.title
