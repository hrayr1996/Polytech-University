from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from administrator.forms import Student as ModelForm
from university.models import fakultet, subject, student, WorkerType, group


@method_decorator(login_required, name='dispatch')
class Add(generic.FormView):
    template_name = 'administrator/student/add.html'
    model = student
    form_class = ModelForm
    success_url = reverse_lazy('aministration:add-student')

    def get_context_data(self, **kwargs):
        context = super(Add, self).get_context_data(**kwargs)
        groups = group.objects.all()

        context['groups'] = groups
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.get('image')
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(Add, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class Edit(generic.UpdateView):
    template_name = 'administrator/student/edit.html'
    model = student
    form_class = ModelForm

    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data(**kwargs)
        student = self.model.objects.get(id=self.kwargs['pk'])
        groups = group.objects.all()

        context['student'] = student
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
            messages.success(self.request, 'Ուսանողի տվյալները հաջողությամբ Խմբագրվել են։')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Սխալ! '+ str(form.errors))
            return self.render_to_response(
              self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('aministration:edit-student', kwargs={'pk':int(self.kwargs['pk'])})

class List(generic.TemplateView):
    template_name = 'administrator/student/index.html'

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        students = student.objects.all()
        request = self.request
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page'] or 1
            if 'students' in request.session:
                request.session['students']['page'] = page
            else:
                request.session['students'] = {}
                request.session['students']['page'] = page
        elif 'students' in request.session:
            if page in request.session.get('students'):
                page = request.session.get('students')['page']

        paginator = Paginator(students, 12)
        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

        context['students'] = students
        context['paginator'] = students
        return context