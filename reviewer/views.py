from django.shortcuts import render, get_object_or_404, redirect
from .models import Card, User, Progress, Category
from django.views import generic
from datetime import datetime, timedelta
from django.utils import timezone

# if something goes wrong with signup/login, it probably should get reincluded here
from . import views_registration
from .views_registration import signup, account_activation_sent, activate, change_password


# home/base-page ( should later identify User/Anonymous and show study-tree accordingly)
def home(request):
    stack = Card.objects.all()
    straf_cats = Category.objects.filter(area='SR')
    oeff_cats = Category.objects.filter(area='OR')
    zr_cats = Category.objects.filter(area='ZR')

    if request.user.is_authenticated:
        cards_to_study = Card.objects.filter(progress__user=request.user, progress__nexttime__lte=timezone.now())
        cards_due = len(cards_to_study)
    else:
        cards_due = 0

    context = {'stack':stack, 'straf_cats':straf_cats, 'oeff_cats':oeff_cats, 'zr_cats':zr_cats, 'cards_due': cards_due}
    return render (request, 'reviewer/home.html', context)


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


# views for the actual studying:
def study_start(request, name, setting):
    #flush old session
    try:
        del request.session['study_list', 'studied_cards', 'known_cards', 'unknown_cards', 'done_list']
    except:
        pass



    # Card objects are retrieved trough chosing category on template
    # first card of the object-list is poped, to be immediatelly passed to study
    if name == 'due':  # the cards which are due to study
        cards_to_study = Card.objects.filter(progress__user=request.user, progress__nexttime__lte=timezone.now()) # __lte stands for less than/equal to following
    elif name == 'due' and setting == 'sr': #cards due in area 'sr'
        cards_to_study = Card.objects.filter(category__area='SR', progress__user=request.user, progress__nexttime__lte=timezone.now())
    elif name == 'due' and setting == 'or':
        cards_to_study = Card.objects.filter(category__area='OR', progress__user=request.user, progress__nexttime__lte=timezone.now())
    elif name == 'due' and setting == 'zr':
        cards_to_study = Card.objects.filter(category__area='ZR', progress__user=request.user, progress__nexttime__lte=timezone.now())
    elif setting == 'cat_due':
        cards_to_study = Card.objects.filter(category__name=name, progress__user=request.user, progress__nexttime__lte=timezone.now())
    else: #simply by category
        cards_to_study = Card.objects.filter(category__name=name)#, progress__nexttime__lte=timezone.now()) # would filter only the ones, which are due

        #if there is no card due, cards_to_study will hold no object

    request.session['studied_cards'] = 0 #counter for studied cards, is retrieved in views.studying_finished and passed to view, set trough buttons
    request.session['known_cards'] = 0
    request.session['unknown_cards'] = 0




    if len(cards_to_study) == 0:
        return redirect('reviewer:studying_finished')
    else:
        # Queryset.pop is not allowed, so workaround:
        first_study_card = cards_to_study[0]
        pk = first_study_card.pk
        #cards_to_study = cards_to_study[1:]
        study_list = []
        for card in cards_to_study:
            study_list.append(card.pk)
            #else:
                #pass
        request.session['study_list'] = study_list

        done_list = [] # creates a list to check off each studied card
        for card in study_list:
            done_list.append(0)
        request.session['done_list'] = done_list


    return redirect('reviewer:studying', pk)    # redirect the list to studying with the pk for the first card to study

def studying(request, pk):

        # get the Card object with the passed pk:
    now_study_card = get_object_or_404(Card, pk=pk)

        # get the list containing the pk's of the cards you want to study out of sessions:
        # next_card_pk is here not really necessary, only in buttons().
    study_list = request.session.get('study_list')
        # atm just for the template, no implicit usage
    done_list = request.session['done_list']

    if len(study_list) == done_list.index(0) + 1:
        next_card_pk = 0
    else:
        next_card_pk = study_list[done_list.index(0) + 1]

        # for the progress bar:
    studied_cards = request.session['studied_cards']
    studying_progress_percent = studied_cards / len(study_list) * 100
    old_stud_prog = (studied_cards - 1) / len(study_list) * 100

    context = {'now_study_card': now_study_card, 'next_card_pk':next_card_pk, 'studying_progress_percent': studying_progress_percent, 'old_stud_prog': old_stud_prog}
    return render (request, 'reviewer/studying.html' , context)

def button(request, button, pk):
    # this function gets the studyied card from the template, changes the according progress depending on
    # which button was pressed an redirects to the studying-view with the next card.pk to study
    card = Card.objects.get(pk=pk)
    if request.user.is_authenticated:
        progress = Progress.objects.get(user=request.user, card=card)
    else:
        pass # request.session['progress'] = {'card.pk': 0, }
    study_list = request.session.get('study_list') # called b/c "not known" button
    done_list = request.session.get('done_list')

    if button == '1': # button "not known", resets card-progress and puts it back in study_list
        if request.user.is_authenticated:
            progress.nexttime = datetime.now() # or timezone.now(), doesnt matter in this case
            progress.progress = 0
        else:
            pass
        study_list.append(card.pk)
        request.session['unknown_cards'] = request.session['unknown_cards'] + 1
        request.session['done_list'].append(0) # so the "counter" at the bottom works

    elif button == '2': # button "hard", starts "short-term"-studying till level 3, then long-term
        if request.user.is_authenticated:
            if progress.progress < 4: # when card was never played, not known or in "short-term"
                progress.nexttime = timezone.now() + timedelta(minutes=5)
            elif progress.progress == 4: # progressing to "long-term"
                progress.nexttime = timezone.now() + timedelta(days=1)
            elif progress.nexttime >= progress.lasttime + timedelta(days=45): #longterm upper border
                progress.nexttime = timezone.now() + timedelta(days=45)
            else: #long-term
                progress.nexttime = timezone.now() + 1.5*(timezone.now() - progress.lasttime) #adds the timedifference from lasttime studyied on top of now() times x
            progress.progress = progress.progress +1
        else:
            pass
        request.session['known_cards'] = request.session['known_cards'] + 1

    elif button == '3': # button "known", starts "short-term"-studying till level 3, then long-term
        if request.user.is_authenticated:
            if progress.progress < 4: # when card was never played, not known or in "short-term"
                progress.nexttime = timezone.now() + timedelta(minutes=5)
            elif progress.progress >3 and progress.progress <=5: # progressing to "long-term"
                progress.nexttime = timezone.now() + timedelta(days=1)
            elif progress.nexttime >= progress.lasttime + timedelta(days=45): #longterm upper border
                progress.nexttime = timezone.now() + timedelta(days=45)
            else: #long-term
                progress.nexttime = timezone.now() + 2*(timezone.now() - progress.lasttime) #adds the timedifference from lasttime studyied on top of now() times x
            progress.progress = progress.progress +2
        else:
            pass
        request.session['known_cards'] = request.session['known_cards'] + 1

    elif button == '4': # button "easy"
        if request.user.is_authenticated:
            if progress.progress < 4:
                progress.nexttime = timezone.now() + timedelta(days=1)
            elif progress.nexttime >= progress.lasttime + timedelta(days=45):# upper-border for study-intervall
                progress.nexttime = timezone.now() + timedelta(days=45)
            else:
                progress.nexttime = timezone.now() + 3*(timezone.now() - progress.lasttime)
            progress.progress = progress.progress +4
        else:
            pass
        request.session['known_cards'] = request.session['known_cards'] + 1

    else:
        pass

    if request.user.is_authenticated:
        progress.save()
    else:
        pass
    request.session['studied_cards'] = request.session['studied_cards'] + 1

    # checks the study_list and prepares the pk for the next view.studying
    # cards are not popped, but a done_list keeps track of studied cards.
    #
    #done_list = request.session.get('done_list'), study_list = request.session.get('study_list'), already called b/c of Button 1


        # b/c .index(0) only shows the first index of 0 workaround:
        # e is a list with all the indexes of the studyied card.pk
        # for the case someone presses button 1 -> pk is appended on study_list
        # e shows therefore both indexes for both, similiar card.pks
        # if the index of the first 0 in the done_list (which is similiar to the study_list) is in e,
        # we know that the second(third/...) card was studied, and can be checked off in done_list
    e = [i for i, j in enumerate(study_list) if j == int(pk)]
    if done_list.index(0) in e:
        done_list[done_list.index(0)] = 1
        request.session['done_list'] = done_list
    else:
        pass
    if 0 not in done_list:  # --> so if all cards are done
        return redirect('reviewer:studying_finished')
    else:
        next_card_pk = study_list[done_list.index(0)]


    return redirect('reviewer:studying', pk=next_card_pk)

def studying_finished(request):
    studied_cards = request.session['studied_cards']
    known_cards = request.session['known_cards']
    unknown_cards = request.session['unknown_cards']
    study_list = request.session['study_list']

    # for the progress bar:
    if studied_cards > 0:
        studying_progress_percent = studied_cards / len(study_list) * 100
        old_stud_prog = (studied_cards - 1) / len(study_list) * 100
    else:
        studying_progress_percent = 100
        old_stud_prog = 0

    context = {'studied_cards': studied_cards, 'known_cards': known_cards, 'unknown_cards': unknown_cards, 'studying_progress_percent': studying_progress_percent, 'old_stud_prog': old_stud_prog}
    return render (request, 'reviewer/studying_finished.html', context)
