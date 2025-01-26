from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# class ProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'profile/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
#         return context

class ProfileCommonView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('users-profile')

class CommonGroupView(PermissionRequiredMixin, View):
    permission_required = 'post.view_posts'

class AuthorGroupView(PermissionRequiredMixin, View):
    permission_required = ('post.view_posts',
                           'post.add_posts',
                           'post.delete_posts')