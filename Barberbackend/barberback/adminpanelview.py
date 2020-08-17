from django.views.generic.edit import *
from django.views.generic.base import *
from django.views.generic.detail import *
from django.views.generic.list import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, views
from django.urls import reverse
from .forms import *


class login(views.LoginView):
    template_name = "barberback/login.html"
    def get_success_url(self):
        return reverse('adminpanel:index')

class logout(views.LogoutView):
    next_page = 'adminpanel:index'


class index(LoginRequiredMixin,TemplateView):
    login_url = '/login'
    redirect_field_name = 'next'
    template_name = 'barberback/index.html'

class successfully(TemplateView):
    template_name = 'barberback/successfully.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if kwargs['number'] == 1:
            context['successfully'] = 'Поздравляем вы успешно ' \
                                      'зарегистрировались в BarberApp !'
        return context



class profile(DetailView):
    model = BarberProfile
    context_object_name = 'profile'
    template_name = 'barberback/profile.html'
    pk_url_kwarg = 'username'

    #Если id записи BarberProfile не совпадает с id записи User
    #то можно использвоать этот код
    #Если совпадает можно закомментировать
    def get_object(self, queryset=None):
        usr = User.objects.get(username = self.kwargs[self.pk_url_kwarg])
        obj = BarberProfile.objects.get(Barber_User = usr)
        return obj

class registUser(FormView):
    form_class = Registration
    template_name = 'barberback/registration.html'

    def form_valid(self, form):
        data = form.cleaned_data

        usr = User()
        usr.username = data['username']
        usr.password = data['password1']
        usr.save()

        usr_profile = BarberProfile()
        usr_profile.Barber_Phone = data['phone']
        usr_profile.Barber_User = usr
        usr_profile.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'adminpanel:successfully',
            kwargs={'number':1}
        )
class listNews(ListView):
    template_name = 'barberback/list_news.html'
    context_object_name = 'news'
    model = BarberNews
    paginate_by = 10
    queryset = BarberNews.objects.all().order_by('-bNewsDate')

class detailNew(DetailView):
    model = BarberNews
    context_object_name = 'new'
    template_name = 'barberback/detail_new.html'

class createNew(CreateView):
    template_name = 'barberback/create_new.html'
    model = BarberNews
    form_class = BNewsForm
    success_url = '/list_news'

    def form_valid(self, form):
        data = form.save()
        data.ChangeImage()
        return super().form_valid(form)


class updateNew(UpdateView):
    template_name = 'barberback/update_new.html'
    model = BarberNews
    form_class = BNewsForm
    success_url = '/list_news'

    def form_valid(self, form):
        data = form.save()
        data.ChangeImage()
        return super().form_valid(form)


class deleteNew(DeleteView):
    model = BarberNews
    template_name = 'barberback/delete_new.html'
    context_object_name = 'new'
    success_url = '/list_news'

    def get_queryset(self):
        return BarberNews.objects.filter(id = self.kwargs[self.pk_url_kwarg])

