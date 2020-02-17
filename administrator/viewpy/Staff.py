from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from Polytech.AuthPerms import is_student
from administrator.forms import Staff as ModelForm
from university.models import fakultet, subject, staff, WorkerType


@method_decorator(login_required, name='dispatch')
class Add(generic.FormView):
    template_name = 'administrator/staff/add.html'
    model = staff
    form_class = ModelForm
    success_url = reverse_lazy('aministration:add-worker')

    def get_context_data(self, **kwargs):
        context = super(Add, self).get_context_data(**kwargs)
        types = WorkerType.objects.all()

        context['workertypes'] = types
        return context

    def form_valid(self, form):
        form.save()
        return super(Add, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class Edit(generic.UpdateView):
    template_name = 'administrator/staff/edit.html'
    model = staff
    form_class = ModelForm

    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data(**kwargs)
        worker = self.model.objects.get(id=self.kwargs['pk'])
        types = WorkerType.objects.all()

        context['worker'] = worker
        context['workertypes'] = types
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
        return reverse_lazy('aministration:edit-worker', kwargs={'pk':int(self.kwargs['pk'])})

class List(generic.TemplateView):
    template_name = 'administrator/staff/index.html'

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        workers = staff.objects.all()
        request = self.request
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page'] or 1
            if 'workers' in request.session:
                request.session['workers']['page'] = page
            else:
                request.session['workers'] = {}
                request.session['workers']['page'] = page
        elif 'workers' in request.session:
            if page in request.session.get('workers'):
                page = request.session.get('workers')['page']

        paginator = Paginator(workers, 12)
        try:
            workers = paginator.page(page)
        except PageNotAnInteger:
            workers = paginator.page(1)
        except EmptyPage:
            workers = paginator.page(paginator.num_pages)

        context['staff'] = workers
        context['paginator'] = workers
        return context