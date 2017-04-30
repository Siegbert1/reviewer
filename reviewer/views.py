from django.shortcuts import render, get_object_or_404, redirect
from .models import Card, User, Progress, Category
from django.views import generic
#from .forms import ProgressForm
# if something goes wrong with signup/login, it probably should get reincluded here
from . import views_registration
from .views_registration import signup, account_activation_sent, activate, change_password
from datetime import datetime, timedelta
from django.utils import timezone

# home/base-page ( should later identify User/Anonymous and show study-tree accordingly)

def home(request):
    stack = Card.objects.all()
    straf_cats = Category.objects.filter(area='SR')
    oeff_cats = Category.objects.filter(area='OR')
    zr_cats = Category.objects.filter(area='ZR')
    context = {'stack':stack, 'straf_cats':straf_cats, 'oeff_cats':oeff_cats, 'zr_cats':zr_cats}
    return render (request, 'reviewer/home.html', context)




#def index(request):
#    stack = Card.objects.all()
#    context = {'stack': stack}
#    return render(request, 'reviewer/index.html', context)

# view for the list of all cards
class IndexView(generic.ListView):
    model = Card
    template_name = 'reviewer/index.html'
    context_object_name = 'stack'

    #not needed b/c 'model = Card' provides that allready
    #def get_queryset(self):
        #return Card.objects.all()


# view for one card
class CardDetail(generic.DetailView):
    model = Card
    #template_name = 'reviewer/card_detail.html'

# view for a list of all the Progress objects of a specified user
class UserCardList(generic.ListView):
    template_name = 'reviewer/cards_by_user.html'
    context_object_name = 'users_cardlist'
    def get_queryset(self):
        self.user_name = get_object_or_404(User, username=self.args[0])
        return Progress.objects.filter(user=self.user_name)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserCardList, self).get_context_data(**kwargs)
        # Get the data from the model and add it to the context, use with {{}} in template
        context['user'] = self.user_name
        context['card'] = Card.objects.all()
        return context

# view of a users Profile
class UserProfile(generic.DetailView):
    model = User
    slug_field = 'username'
    template_name = 'reviewer/user_profile.html'

# view for the actual studying


def study_start(request, name):
    #flush old session
    try:
        del request.session['study_list']
    except:
        pass
    # Card objects are retrieved trough chosing category on template
    # first card of the object-list is poped, to be immediatelly passed to study
    if name == 'due':  # the cards which are due to study
        cards_to_study = Card.objects.filter(progress__user=request.user, progress__nexttime__lte=timezone.now()) # __lte stands for less than/equal to following
    else:
        cards_to_study = Card.objects.filter(category__name=name) # could be used to get different data set through slug or similar
    # Queryset.pop is not allowed, so workaround:
    first_study_card = cards_to_study[0]
    cards_to_study = cards_to_study[1:]
    study_list = []
    for card in cards_to_study:
        #check if card is due to study
        #card_progress = Progress.objects.get(user=request.user, card=card)
        #if card_progress.nexttime <= datetime.now():
        study_list.append(card.pk)
        #else:
            #pass
    request.session['study_list'] = study_list
    # insert mechanism to only get the cards, which should be studied from the stack in regards to "progress_lasttime"


    return redirect('reviewer:studying', first_study_card.pk)    # redirect the list to studying with the pl for the first card to study



def studying(request, pk):
    if pk == '0':
        return redirect('reviewer:studying_finished')
    else:
        #get the Card object with the passed pk:
        now_study_card = get_object_or_404(Card, pk=pk)
        # after playing in (else), progress is processed and the next card is drawn
        progress = Progress.objects.get(user=request.user, card=now_study_card)

        #get the list containing the pk's of the cards you want to study out of sessions:
        # next_card_pk is here not really necessary, only in buttons().
        study_list = request.session.get('study_list')
        if len(study_list) == 0:
            next_card_pk = 0
        else:
            next_card_pk = study_list[0]


        context = {'now_study_card': now_study_card, 'next_card_pk':next_card_pk}
        return render (request, 'reviewer/studying.html' , context)

def button(request, button, pk):
    # this function gets the studyied card from the template, changes the according progress depending on
    # which button was pressed an redirects to the studying-view with the next card.pk to study
    card = Card.objects.get(pk=pk)
    progress = Progress.objects.get(user=request.user, card=card)
    study_list = request.session.get('study_list')
    if button == '1': # button "not known", resets card-progress

        progress.nexttime = datetime.now() # or timezone.now(), doesnt matter in this case
        progress.progress = 0
        study_list.append(card.pk)
    elif button == '2': # button "known", starts "short-term"-studying till level 3, then long-term
        if progress.progress < 2: # when card was never played, not known or in "short-term"
            progress.nexttime = timezone.now() + timedelta(minutes=5)
        elif progress.progress == 2: # progressing to "long-term"
            progress.nexttime = timezone.now() + timedelta(days=1)
        elif progress.nexttime >= progress.lasttime + timedelta(days=45): #longterm upper border
            progress.nexttime = timezone.now() + timedelta(days=45)
        else: #long-term
            progress.nexttime = timezone.now() + 2*(timezone.now() - progress.lasttime) #adds the timedifference from lasttime studyied on top of now() times x
        progress.progress = progress.progress +1

    elif button == '3': # button "easy"
        if progress.progress < 2:
            progress.nexttime = timezone.now() + timedelta(days=1)
        elif progress.nexttime >= progress.lasttime + timedelta(days=45):# upper-border for study-intervall
            progress.nexttime = timezone.now() + timedelta(days=45)
        else:
            progress.nexttime = timezone.now() + 3*(timezone.now() - progress.lasttime)
        progress.progress = progress.progress +2

    else:
        pass

    progress.save()
    #study_list = request.session.get('study_list'), already called
    if len(study_list) == 0:
        next_card_pk = 0
    else:
        next_card_pk = study_list.pop(0)
        request.session['study_list']= study_list
    return redirect('reviewer:studying', pk=next_card_pk)

def studying_finished(request):
    context = {}
    return render (request, 'reviewer/studying_finished.html', context)
