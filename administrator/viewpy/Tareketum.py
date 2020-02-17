from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from administrator.forms import Subject as ModelForm
from university.models import subject as CurModel
from university.models import fakultet, subject, student, WorkerType, group


@method_decorator(login_required, name='dispatch')
class Add(generic.FormView):
    template_name = 'administrator/subject/add.html'
    model = CurModel
    form_class = ModelForm
    success_url = reverse_lazy('aministration:add-tareketum')

    def get_context_data(self, **kwargs):
        context = super(Add, self).get_context_data(**kwargs)
        groups = group.objects.all()

        context['groups'] = groups
        return context

    def form_valid(self, form):
        form.save()
        return super(Add, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class Edit(generic.UpdateView):
    template_name = 'administrator/subject/edit.html'
    model = CurModel
    form_class = ModelForm

    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data(**kwargs)
        worker = self.model.objects.get(id=self.kwargs['pk'])
        groups = group.objects.all()

        context['worker'] = worker
        context['groups'] = groups
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
            messages.success(self.request, 'Աշխատողը հաջողությամբ Խմբագրվել է։')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Սխալ! '+ str(form.errors))
            return self.render_to_response(
              self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('aministration:edit-tareketum', kwargs={'pk':int(self.kwargs['pk'])})

class List(generic.TemplateView):
    template_name = 'administrator/subject/index.html'

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        subjects = CurModel.objects.all()
        request = self.request
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page'] or 1
            if 'subjects' in request.session:
                request.session['subjects']['page'] = page
            else:
                request.session['subjects'] = {}
                request.session['subjects']['page'] = page
        elif 'subjects' in request.session:
            if page in request.session.get('subjects'):
                page = request.session.get('subjects')['page']

        paginator = Paginator(subjects, 12)
        try:
            subjects = paginator.page(page)
        except PageNotAnInteger:
            subjects = paginator.page(1)
        except EmptyPage:
            subjects = paginator.page(paginator.num_pages)

        context['subjects'] = subjects
        context['paginator'] = subjects
        return context