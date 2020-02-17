from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from administrator.forms import Fakultet as ModelForm
from university.models import  staff, fakultet


@method_decorator(login_required, name='dispatch')
class Add(generic.FormView):
    template_name = 'administrator/fakultet/add.html'
    model = fakultet
    form_class = ModelForm
    success_url = reverse_lazy('aministration:add-fakultet')

    def get_context_data(self, **kwargs):
        context = super(Add, self).get_context_data(**kwargs)
        workers = staff.objects.filter(type=1)
        context['workers'] = workers
        return context

    def form_valid(self, form):
        form.save()
        return super(Add, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class Edit(generic.UpdateView):
    template_name = 'administrator/fakultet/edit.html'
    model = fakultet
    form_class = ModelForm

    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data(**kwargs)
        fakultet = self.model.objects.get(id=self.kwargs['pk'])
        workers = staff.objects.filter(type=1)
        context['fakultet'] = fakultet
        context['workers'] = workers
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
            messages.success(self.request, 'Ֆակուլտետը հաջողությամբ Խմբագրվել է։')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Սխալ! '+ str(form.errors))
            return self.render_to_response(
              self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('aministration:edit-fakultet', kwargs={'pk':int(self.kwargs['pk'])})

class List(generic.TemplateView):
    template_name = 'administrator/fakultet/index.html'

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        fakultetlist = fakultet.objects.all()
        request = self.request
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page'] or 1
            if 'fakultets' in request.session:
                request.session['fakultets']['page'] = page
            else:
                request.session['fakultets'] = {}
                request.session['fakultets']['page'] = page
        elif 'fakultets' in request.session:
            if page in request.session.get('fakultets'):
                page = request.session.get('fakultets')['page']

        paginator = Paginator(fakultetlist, 12)
        try:
            fakultetlist = paginator.page(page)
        except PageNotAnInteger:
            fakultetlist = paginator.page(1)
        except EmptyPage:
            fakultetlist = paginator.page(paginator.num_pages)

        context['fakultets'] = fakultetlist
        context['paginator'] = fakultetlist
        return context