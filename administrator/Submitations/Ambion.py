from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.decorators.http import require_http_methods


class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

@require_http_methods(["GET", "POST"])
class Ambion(LoginRequiredMixin, generic.TemplateViw):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

