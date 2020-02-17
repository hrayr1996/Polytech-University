from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from administrator.forms import Exam as ModelForm
from university.models import Exam as CurModel
from university.models import fakultet, subject, student, WorkerType, group


@method_decorator(login_required, name='dispatch')
class Add(generic.FormView):
    template_name = 'administrator/exam/add.html'
    model = CurModel
    form_class = ModelForm
    success_url = reverse_lazy('aministration:add-exam')

    def get(self, request, *args, **kwargs):
        super(Add, self).get(request, *args, **kwargs)
        form = self.form_class()
        return self.render_to_response(self.get_context_data( form=form))

    def form_valid(self, form):
        form.save()
        return super(Add, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class Edit(generic.UpdateView):
    template_name = 'administrator/exam/edit.html'
    model = CurModel
    form_class = ModelForm

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
            messages.success(self.request, 'Քննությունը հաջողությամբ Խմբագրվել է։')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Սխալ! '+ str(form.errors))
            return self.render_to_response(
              self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('aministration:edit-exam', kwargs={'pk':int(self.kwargs['pk'])})

class List(generic.TemplateView):
    template_name = 'administrator/exam/index.html'

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        exams = CurModel.objects.all()
        request = self.request
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page'] or 1
            if 'exams' in request.session:
                request.session['exams']['page'] = page
            else:
                request.session['exams'] = {}
                request.session['exams']['page'] = page
        elif 'exams' in request.session:
            if page in request.session.get('exams'):
                page = request.session.get('exams')['page']

        paginator = Paginator(exams, 12)
        try:
            exams = paginator.page(page)
        except PageNotAnInteger:
            exams = paginator.page(1)
        except EmptyPage:
            exams = paginator.page(paginator.num_pages)

        context['exams'] = exams
        context['paginator'] = exams
        return context