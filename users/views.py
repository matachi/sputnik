from django.contrib.auth import get_user_model
from django.views.generic import DetailView, UpdateView
from users.models import PersonalUserProfile


class Profile(DetailView):
    template_name = 'users/profile.html'

    def get_object(self):
        self.user = get_user_model().objects.get(
            username=self.kwargs['username'])
        return self.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal_profile'] = self.user.personal_profile
        return context


class Settings(UpdateView):
    template_name = 'users/settings.html'
    fields = ['website', 'twitter', 'facebook', 'github', 'bitbucket',
              'visible_email']

    def get_object(self):
        return self.request.user.personal_profile
