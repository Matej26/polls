from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Question, Choice, Profile
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import RegistrationForm, EditAccountForm, CreatePollForm
from django.contrib.auth import views


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


class RegistrationView(generic.FormView):
    template_name = 'registration/registration.html'

    def dispatch(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password']
                password2 = form.cleaned_data['confirm_password']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                if password1 == password2:
                    user = User.objects.create_user(username, email, password1)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    Profile.objects.create(user=user)
                    return redirect('/polls/login')

        return render(request, self.template_name, {'form': form})


class LoginView(views.LoginView):
    template_name = 'registration/login.html'


class LogoutView(views.LogoutView):
    template_name = 'registration/logout.html'


@login_required
def account(request):
    return HttpResponseRedirect(reverse('polls:user_account', args=(request.user.id,)))


@login_required
def user_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # if request.user.id == user_id:
    return render(request, 'polls/account.html', {'user': user})
    # else:
    #     return render(request, 'polls/not_my_acc.html', {'user': user})


@login_required
def edit_account(request, user_id):
    if request.user.id == user_id:
        form = EditAccountForm(request.POST)
        set_initials(form, request.user)
        if request.method == 'POST':
            if form.is_valid():
                request.user.username = form.cleaned_data['username'] \
                    if form.cleaned_data['username'] != '' else form.fields['username'].initial
                request.user.email = form.cleaned_data['email'] \
                    if form.cleaned_data['email'] != '' else form.fields['email'].initial
                request.user.first_name = form.cleaned_data['first_name'] \
                    if form.cleaned_data['first_name'] != '' else form.fields['first_name'].initial
                request.user.last_name = form.cleaned_data['last_name'] \
                    if form.cleaned_data['last_name'] != '' else form.fields['last_name'].initial
                request.user.profile.bio = form.cleaned_data['bio']
                request.user.save()
                request.user.profile.save()
                return redirect('/polls/account')
        return render(request, 'polls/edit.html', {'form': form})
    else:
        return redirect('/polls/account/'+str(user_id))


@login_required
def create(request, user_id):
    if request.user.id == user_id:
        form = CreatePollForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                text = form.cleaned_data['question']
                q = Question(profile=request.user.profile, question_text=text, pub_date=timezone.now())
                q.save()
                c1 = Choice(question=q, choice_text=form.cleaned_data['choice1'])
                c1.save()
                c2 = Choice(question=q, choice_text=form.cleaned_data['choice2'])
                c2.save()
                if form.cleaned_data['choice3'] != '':
                    c3 = Choice(question=q, choice_text=form.cleaned_data['choice3'])
                    c3.save()
                if form.cleaned_data['choice4'] != '':
                    c4 = Choice(question=q, choice_text=form.cleaned_data['choice4'])
                    c4.save()
                if form.cleaned_data['choice5'] != '':
                    c5 = Choice(question=q, choice_text=form.cleaned_data['choice5'])
                    c5.save()
                return redirect('/polls/account')
        return render(request, 'polls/create.html', {'form': form})
    else:
        return redirect('/polls/account/' + str(user_id))


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


@login_required
def delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user.id == question.profile.user.id:
        question.delete()
    return redirect('/polls/')


def set_initials(form, user):
    form.fields['username'].initial = user.username
    form.fields['email'].initial = user.email
    form.fields['first_name'].initial = user.first_name
    form.fields['last_name'].initial = user.last_name
