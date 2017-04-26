from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from .models import Card, User, Progress
from django.views import generic
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import account_activation_token

#for signup/ login
from django.contrib.auth import login, authenticate
# Create your views here.

from django.contrib.auth import get_user_model
User = get_user_model()

# home/base-page ( should later identify User/Anonymous and show study-tree accordingly)

def home(request):
    stack = Card.objects.all()
    context = {'stack':stack}
    return render (request, 'reviewer/home.html', context)



# because User is custom (needed for signup form)
from django.contrib.auth.forms import UserCreationForm
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields

# for signup of the user
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('reviewer:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('reviewer:home')
    else:
        return render(request, 'registration/account_activation_invalid.html')




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
