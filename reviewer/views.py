from django.shortcuts import render, get_object_or_404
from .models import Card, User, Progress
from django.views import generic
# Create your views here.

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

# view for the actual
