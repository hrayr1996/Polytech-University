from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from administrator.forms import Matyan as ModelForm
from university.models import staff, profession, matyan, group, student


@method_decorator(login_required, name='dispatch')
class Add(generic.FormView):
    template_name = 'administrator/matyan/add.html'
    model = matyan
    form_class = ModelForm
    success_url = reverse_lazy('aministration:add-matyan')

    def get_context_data(self, **kwargs):
        context = super(Add, self).get_context_data(**kwargs)
        groups = group.objects.filter()
        students = student.objects.all()

        context['groups'] = groups
        context['students'] = students
        return context

    def form_valid(self, form):
        form.save()
        return super(Add, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class Edit(generic.UpdateView):
    template_name = 'administrator/matyan/edit.html'
    model = matyan
    form_class = ModelForm

    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data(**kwargs)
        matyan = self.model.objects.get(id=self.kwargs['pk'])
        groups = group.objects.filter()
        students = student.objects.all()

        context['matyan'] = matyan
        context['groups'] = groups
        context['students'] = students
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
            messages.success(self.request, 'Մատյանը հաջողությամբ Թարմացվել է։')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Սխալ! '+ str(form.errors))
            return self.render_to_response(
              self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('aministration:edit-matyan', kwargs={'pk':int(self.kwargs['pk'])})

class List(generic.TemplateView):
    template_name = 'administrator/matyan/index.html'

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        matyanlist = matyan.objects.all()
        request = self.request
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page'] or 1
            if 'matyans' in request.session:
                request.session['matyans']['page'] = page
            else:
                request.session['matyans'] = {}
                request.session['matyans']['page'] = page
        elif 'matyans' in request.session:
            if page in request.session.get('matyans'):
                page = request.session.get('matyans')['page']

        paginator = Paginator(matyanlist, 12)
        try:
            matyanlist = paginator.page(page)
        except PageNotAnInteger:
            matyanlist = paginator.page(1)
        except EmptyPage:
            matyanlist = paginator.page(paginator.num_pages)

        context['matyans'] = matyanlist
        context['paginator'] = matyanlist
        return context