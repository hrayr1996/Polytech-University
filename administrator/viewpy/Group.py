from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from administrator.forms import Group as ModelForm
from university.models import staff,  group, profession


@method_decorator(login_required, name='dispatch')
class Add(generic.FormView):
    template_name = 'administrator/group/add.html'
    model = group
    form_class = ModelForm
    success_url = reverse_lazy('aministration:add-group')

    def get_context_data(self, **kwargs):
        context = super(Add, self).get_context_data(**kwargs)
        workers = staff.objects.filter(type=1)
        professions = profession.objects.all()

        context['workers'] = workers
        context['professions'] = professions
        return context

    def form_valid(self, form):
        form.save()
        return super(Add, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class Edit(generic.UpdateView):
    template_name = 'administrator/group/edit.html'
    model = group
    form_class = ModelForm

    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data(**kwargs)
        group = self.model.objects.get(id=self.kwargs['pk'])
        workers = staff.objects.filter(type=1)
        professions = profession.objects.all()

        context['group'] = group
        context['workers'] = workers
        context['professions'] = professions
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
            messages.success(self.request, 'Խումբը հաջողությամբ Խմբագրվել է։')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Սխալ! '+ str(form.errors))
            return self.render_to_response(
              self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('aministration:edit-group', kwargs={'pk':int(self.kwargs['pk'])})

class List(generic.TemplateView):
    template_name = 'administrator/group/index.html'

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        grouplist = group.objects.all()
        request = self.request
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page'] or 1
            if 'groups' in request.session:
                request.session['groups']['page'] = page
            else:
                request.session['groups'] = {}
                request.session['groups']['page'] = page
        elif 'groups' in request.session:
            if page in request.session.get('groups'):
                page = request.session.get('groups')['page']

        paginator = Paginator(grouplist, 12)
        try:
            grouplist = paginator.page(page)
        except PageNotAnInteger:
            grouplist = paginator.page(1)
        except EmptyPage:
            grouplist = paginator.page(paginator.num_pages)

        context['groups'] = grouplist
        context['paginator'] = grouplist
        return context