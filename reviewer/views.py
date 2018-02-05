from django.shortcuts import render, get_object_or_404, redirect
from .models import Card, User, Progress, Category, Case_ZR
from django.views import generic
from datetime import datetime, timedelta
from django.utils import timezone
from .forms import CaseForm_ZR, CheckForm_ZR
# if something goes wrong with signup/login, it probably should get reincluded here
from . import views_registration
from .views_registration import signup, account_activation_sent, activate, change_password

from django.http import HttpResponse
# home/base-page ( should later identify User/Anonymous and show study-tree accordingly)
def home(request):
    stack = Card.objects.all()
    straf_cats = Category.objects.filter(area='SR')
    oeff_cats = Category.objects.filter(area='OR')
    zr_cats = Category.objects.filter(area='ZR')

    context = {'stack':stack, 'straf_cats':straf_cats, 'oeff_cats':oeff_cats, 'zr_cats':zr_cats}

    if request.user.is_authenticated:
        cards_to_study = Card.objects.filter(progress__user=request.user, progress__nexttime__lte=timezone.now(), progress__progress__gt=0)
        cards_due = len(cards_to_study)
         # for the progress bars of the single categorys
        dic = {}
        for cat in Category.objects.all():
            #worth is int, could be changed to reflect progress_level
            worth = len(Progress.objects.filter(user=request.user, card__category=cat, progress__gt=0))/int(cat.containing_cards) *100
            dic[cat.pk] = worth
        context['dic'] = dic

    else:
        cards_due = 0

    context['cards_due'] = cards_due
    return render (request, 'reviewer/home.html', context)

def contact(request):
    return render (request, 'reviewer/contact.html')


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
def UserProfile(request, pk):
    user = request.user
    #slug_field = 'username'
    #template_name = 'reviewer/user_profile.html'
    context = {}

    straf_all = len(Progress.objects.filter(user=request.user, card__category__area="SR"))
    straf_longtime = len(Progress.objects.filter(user=request.user, card__category__area="SR", progress__gt=4))
    straf_shorttime = len(Progress.objects.filter(user=request.user, card__category__area="SR", progress__gt=0, progress__lt=5))
    straf_rest = straf_all - straf_longtime - straf_shorttime
    context['progress_straf_longtime'] = straf_longtime
    context['progress_straf_shorttime'] = straf_shorttime
    context['progress_straf_rest'] = straf_rest
    context['progress_straf_longtime_percent'] = int(round(straf_longtime/straf_all *100, 0))
    context['progress_straf_shorttime_percent'] = int(round(straf_shorttime/straf_all *100, 0))
    context['progress_straf_rest_percent'] = int(round(straf_rest/straf_all *100, 0))

    oeff_all = len(Progress.objects.filter(user=request.user, card__category__area="OR"))
    oeff_longtime = len(Progress.objects.filter(user=request.user, card__category__area="OR", progress__gt=4))
    oeff_shorttime = len(Progress.objects.filter(user=request.user, card__category__area="OR", progress__gt=0, progress__lt=5))
    oeff_rest = oeff_all - oeff_longtime - oeff_shorttime
    context['progress_oeff_longtime'] = oeff_longtime
    context['progress_oeff_shorttime'] = oeff_shorttime
    context['progress_oeff_rest'] = oeff_rest
    context['progress_oeff_longtime_percent'] = int(round(oeff_longtime/oeff_all *100, 0))
    context['progress_oeff_shorttime_percent'] = int(round(oeff_shorttime/oeff_all *100, 0))
    context['progress_oeff_rest_percent'] = int(round(oeff_rest/oeff_all *100, 0))

    zr_all = len(Progress.objects.filter(user=request.user, card__category__area="ZR"))
    zr_longtime = len(Progress.objects.filter(user=request.user, card__category__area="ZR", progress__gt=4))
    zr_shorttime = len(Progress.objects.filter(user=request.user, card__category__area="ZR", progress__gt=0, progress__lt=5))
    zr_rest = zr_all - zr_longtime - zr_shorttime
    context['progress_zr_longtime'] = zr_longtime
    context['progress_zr_shorttime'] = zr_shorttime
    context['progress_zr_rest'] = zr_rest
    context['progress_zr_longtime_percent'] = int(round(zr_longtime/zr_all *100, 0))
    context['progress_zr_shorttime_percent'] = int(round(zr_shorttime/zr_all *100, 0))
    context['progress_zr_rest_percent'] = int(round(zr_rest/zr_all *100, 0))

    return render(request, 'reviewer/user_profile.html', context)

# views for the actual studying:
def study_start(request, name, setting):
    #flush old session
    try:
        del request.session['study_list', 'studied_cards', 'known_cards', 'unknown_cards', 'done_list']
    except:
        pass



    # Card objects are retrieved trough chosing category on template
    # first card of the object-list is poped, to be immediatelly passed to study
    if name == 'due':  # the cards which are due to study and at least one time studied
        cards_to_study = Card.objects.filter(progress__user=request.user, progress__nexttime__lte=timezone.now(), progress__progress__gt=0) # __lte stands for less than/equal to following, gt greater than
    elif name == 'due' and setting == 'sr': #cards due in area 'sr'
        cards_to_study = Card.objects.filter(category__area='SR', progress__user=request.user, progress__nexttime__lte=timezone.now(), progress__progress__gt=0)
    elif name == 'due' and setting == 'or':
        cards_to_study = Card.objects.filter(category__area='OR', progress__user=request.user, progress__nexttime__lte=timezone.now(), progress__progress__gt=0)
    elif name == 'due' and setting == 'zr':
        cards_to_study = Card.objects.filter(category__area='ZR', progress__user=request.user, progress__nexttime__lte=timezone.now(), progress__progress__gt=0)

    # for cards which have never been studied and so have a progress of 0 (not known sets porgress = 1)
    elif setting == 'not_studied':
        cards_to_study = Card.objects.filter(category__name=name, progress__user=request.user, progress__progress=0)


    elif setting == 'cat_due':
        cards_to_study = Card.objects.filter(category__name=name, progress__user=request.user, progress__nexttime__lte=timezone.now())
    else: #simply by category
        cards_to_study = Card.objects.filter(category__name=name)#, progress__nexttime__lte=timezone.now()) # would filter only the ones, which are due

        #if there is no card due, cards_to_study will hold no object

    request.session['studied_cards'] = 0 #counter for studied cards, is retrieved in views.studying_finished and passed to view, set trough buttons
    request.session['known_cards'] = 0
    request.session['unknown_cards'] = 0
    request.session['study_list'] = []



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
    studying_progress_percent = round((studied_cards / len(study_list) * 100), 0) # cuts off the %16,66666666666 tail
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
            progress.progress = 1
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
                progress.nexttime = timezone.now() + 1.5*(timezone.now() - progress.lasttime) #adds the timedifference from lasttime studyied on top of now() times 1.5
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
        studying_progress_percent = round((studied_cards / len(study_list) * 100), 0)
        old_stud_prog = (studied_cards - 1) / len(study_list) * 100
    else:
        studying_progress_percent = 100
        old_stud_prog = 0

    context = {'studied_cards': studied_cards, 'known_cards': known_cards, 'unknown_cards': unknown_cards, 'studying_progress_percent': studying_progress_percent, 'old_stud_prog': old_stud_prog}
    return render (request, 'reviewer/studying_finished.html', context)



def case_creation(request, area):
# get the right area-key for the model and Form
    if request.method == 'POST':
        if area == "zr":
            form = CaseForm_ZR(request.POST)
        elif area == "sr":
            form = CaseForm_ZR(request.POST) #CaseForm_SR
        else: # area == "or"
            form = CaseForm_ZR(request.POST) #CaseForm_OR

# work the form and data
        if form.is_valid():
            form.process()
            case = form.save(commit=False)
            string = form.cleaned_data['string']
            case.solution = string

            case.owner = request.user
            case.save()

        return redirect('reviewer:home')
    else:
        if area == "zr":
            form = CaseForm_ZR()
        elif area == "sr":
            form = CaseForm_ZR() #CaseForm_SR
        else: # area == "or"
            form = CaseForm_ZR() #CaseForm_OR

    return render (request, 'reviewer/case_creation_zr.html', {'form': form})



def case_edit(request, pk, area):
    if area == "zr":
        case = get_object_or_404(Case_ZR, pk=pk)
    elif area == "sr":
        case = get_object_or_404(Case_ZR, pk=pk) #Case_SR
    else: #area == "or":
        case = get_object_or_404(Case_ZR, pk=pk) #Case_OR

    if request.method == "POST":
        if area == "zr":
            form = CaseForm_ZR(request.POST, instance=case)
        elif area == "sr":
            form = CaseForm_ZR(request.POST, instance=case)
        else: #area == "or":
            form = CaseForm_ZR(request.POST, instance=case)
        if form.is_valid():
            form.process()
            case = form.save(commit=False)
            string = form.cleaned_data['string']
            case.solution = string

            case.owner = request.user
            case.save()

        return redirect('reviewer:home')
    else:
        if area == "zr":
            form = CaseForm_ZR(instance=case)
            return render(request, 'reviewer/case_creation_zr.html', {'form': form,})
        elif area == "sr":
            form = CaseForm_ZR(instance=case)
            return render(request, 'reviewer/case_creation_zr.html', {'form': form,})
        else: #area == "or":
            form = CaseForm_ZR(instance=case)
            return render(request, 'reviewer/case_creation_zr.html', {'form': form,})



def case_reviewer(request, pk, area):
        if area == "zr":
            case = get_object_or_404(Case_ZR, pk=pk)
        elif area == "sr":
            case = get_object_or_404(Case_ZR, pk=pk) #Case_SR
        else: #area == "or":
            case = get_object_or_404(Case_ZR, pk=pk) #Case_OR
        context = {'case': case}

        if request.method == "POST":
            if area == "zr":
                form = CheckForm_ZR(request.POST, instance=case)
            elif area == "sr":
                form = CheckForm_ZR(request.POST, instance=case)
            else: #area == "or":
                form = CheckForm_ZR(request.POST, instance=case)
            if form.is_valid():
                form.process()
                string = form.cleaned_data['answer_string']
                request.session['answer_string'] = string

            return redirect('reviewer:case_finished', pk=pk, area=area) # should redirect to finished

        else:
            if area == "zr":
                form = CheckForm_ZR()
                template = 'reviewer/case_reviewer_zr.html'
                context['form'] = form

            elif area == "sr":
                form = CheckForm_ZR()
                template = 'reviewer/case_reviewer_zr.html'
                context['form'] = form
            else: #area == "or":
                form = CheckForm_ZR()
                template = 'reviewer/case_reviewer_zr.html'
                context['form'] = form
            return render(request, template, context)

# should take done case-form and show right solution and WRONG/RIGHT
def case_finished(request, pk, area):
    if area == "zr":
        case = get_object_or_404(Case_ZR, pk=pk)
    elif area == "sr":
        case = get_object_or_404(Case_ZR, pk=pk) #Case_SR
    else: #area == "or":
        case = get_object_or_404(Case_ZR, pk=pk) #Case_OR

    answer_string = request.session['answer_string']
    context = {'case': case}
    if str(answer_string) == str(case.solution):
        context['correct'] = True
    else:
        context['correct'] = False
    context['answerstr'] = answer_string

    # compares answer and solution strings and outputs the indices of the not-equal letters in a list
    x = answer_string
    y = case.solution
    wrong = [i for i in range(len(x)) if x[i] != y[i]]
    # give wrong answers to template to mark them as such  (they are in the template as wrong0, wrong1, wrong2, but only the ones which are truly wrong, so only check for existance)
    for number in wrong:
        name = "wrong" + str(number)
        context[name] = True

    if area == "zr":
        form = CheckForm_ZR(instance=case)
        template = 'reviewer/case_finished_zr.html'
        context['form'] = form

    elif area == "sr":
        form = CheckForm_ZR(instance=case)
        template = 'reviewer/case_finished_zr.html'
        context['form'] = form
    else: #area == "or":
        form = CheckForm_ZR(instance=case)
        template = 'reviewer/case_finished_zr.html'
        context['form'] = form

    return render(request, template, context)
