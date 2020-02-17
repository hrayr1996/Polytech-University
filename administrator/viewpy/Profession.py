from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from administrator.forms import Profession as ModelForm
from university.models import profession, fakultet, subject


@method_decorator(login_required, name='dispatch')
class Add(generic.FormView):
    template_name = 'administrator/profession/add.html'
    model = profession
    form_class = ModelForm
    success_url = reverse_lazy('aministration:add-profession')

    def get_context_data(self, **kwargs):
        context = super(Add, self).get_context_data(**kwargs)
        fakultets = fakultet.objects.filter()
        subjects = subject.objects.all()

        context['subjects'] = subjects
        context['fakultets'] = fakultets
        return context

    def form_valid(self, form):
        form.save()
        return super(Add, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class Edit(generic.UpdateView):
    template_name = 'administrator/profession/edit.html'
    model = profession
    form_class = ModelForm

    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data(**kwargs)
        profession = self.model.objects.get(id=self.kwargs['pk'])
        fakultets = fakultet.objects.filter(type=1)
        subjects = subject.objects.all()

        context['profession'] = profession
        context['fakultets'] = fakultets
        context['subjects'] = subjects
        return context

    def get(self, request, *args, **kwargs):
        super(Edit, self).get(request, *args, **kwargs)
        form = self.form_class(instance=self.object)
        return self.render_to_response(self.get_context_data(
            object=self.object, form=form))

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST or None, instance=self.object)

        if form.is_valid():
            form.save()
            messages.success(self.request, 'Մասնագիտությունը հաջողությամբ Խմբագրվել է։')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Սխալ! '+ str(form.errors))
            return self.render_to_response(
              self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('aministration:edit-profession', kwargs={'pk':int(self.kwargs['pk'])})

class List(generic.TemplateView):
    template_name = 'administrator/profession/index.html'

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        professions = profession.objects.all()
        request = self.request
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page'] or 1
            if 'professions' in request.session:
                request.session['professions']['page'] = page
            else:
                request.session['professions'] = {}
                request.session['professions']['page'] = page
        elif 'professions' in request.session:
            if page in request.session.get('professions'):
                page = request.session.get('professions')['page']

        paginator = Paginator(professions, 12)
        try:
            professions = paginator.page(page)
        except PageNotAnInteger:
            professions = paginator.page(1)
        except EmptyPage:
            professions = paginator.page(paginator.num_pages)

        context['professions'] = professions
        context['paginator'] = professions
        return context