from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, resolve
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, DeleteView, UpdateView

from accounts.models import BaseUser
from database.forms import get_dynamic_model_form, get_dynamic_model_choice_set_form
from database.models.relationships import Preference
from database.models.schedule_models import Course, Section, Schedule, Timeblock
from database.models.structural_models import Department, ModelSet, SetMembership
from database.models.user_models import Student, Teacher


class DynamicModelMixin(object):
    dynamic_model = None
    dynamic_model_name = None
    model_map_dict = {
        'students': Student,
        'teachers': Teacher,
        'preferences': Preference,
        'departments': Department,
        'schedules': Schedule,
        'courses': Course,
        'sections': Section,
        'timeblocks': Timeblock,
        'model-set': ModelSet,
    }

    def dispatch(self, request, *args, **kwargs):
        self.dynamic_model_name = kwargs.get('model')
        dynamic_model = self.model_map_dict.get(self.dynamic_model_name, None)
        if dynamic_model:
            self.dynamic_model = dynamic_model
            return super().dispatch(request, args, kwargs)
        raise Http404


class CrudUsersView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/crud_users.html'


class CrudSetsView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/crud_sets.html'


class CrudConstraintsView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/crud_constraints.html'


class CrudSchedulingView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/crud_scheduling.html'


class CrudDeleteView(LoginRequiredMixin, DynamicModelMixin, DeleteView):
    template_name = "crud/generic_delete_view.html"

    def get_object(self):
        return get_object_or_404(self.dynamic_model, pk=self.kwargs.get('id'))

    def get_success_url(self):
        return reverse('database:crud_model', kwargs={'model': self.dynamic_model_name})


class CrudInspectView(LoginRequiredMixin, DynamicModelMixin, DeleteView):
    template_name = "crud/generic_inspection_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_data'] = serialize("python", [self.object], use_natural_foreign_keys=True)
        return context

    def get_object(self, **kwargs):
        return get_object_or_404(self.dynamic_model, pk=self.kwargs.get('id'))

    def get_success_url(self):
        return reverse('database:crud_model', kwargs={'model': self.dynamic_model_name})


class CrudUpdateView(LoginRequiredMixin, DynamicModelMixin, UpdateView):
    template_name = "crud/generic_update_view.html"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(CrudUpdateView, self).get_context_data(**kwargs)
        if self.dynamic_model in [Student, Teacher]:
            user_object = BaseUser.objects.filter(pk=self.object.user_id)[0]
            context['form'] = self.get_form_class()(
                instance=self.object,
                initial={
                    'first_name': user_object.first_name,
                    'last_name': user_object.last_name,
                    'email': user_object.email
                })
        return context

    def get_form_class(self):
        return get_dynamic_model_form(self.dynamic_model)

    def get_object(self, **kwargs):
        return get_object_or_404(self.dynamic_model, pk=self.kwargs.get('id'))

    def get_success_url(self):
        return reverse('database:crud_model', kwargs={'model': self.dynamic_model_name})


class CrudView(LoginRequiredMixin, DynamicModelMixin, FormView):
    template_name = "crud/generic_crud_view.html"
    context_object_name = 'all_objects'

    def get_form_class(self):
        return get_dynamic_model_form(self.dynamic_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'all_objects': self.dynamic_model.objects.all(),
            'dynamic_model_name': self.dynamic_model_name
        })
        return context

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DynamicModelSetCreateView(LoginRequiredMixin, DynamicModelMixin, FormView):
    template_name = "crud/generic_crud_view.html"
    context_object_name = 'all_objects'

    def get_form_class(self):
        return get_dynamic_model_choice_set_form(self.dynamic_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'all_objects': ModelSet.objects.filter(
                setmembership__content_type__model=self.dynamic_model.__name__.lower()
            ).distinct(),
            'dynamic_model_name': self.dynamic_model_name,
            'url_name': resolve(self.request.path_info).url_name
        })

        return context

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        SetMembership.objects.bulk_create([
            SetMembership(
                set=form.cleaned_data['set'],
                member_object=choice
            )
            for choice in form.cleaned_data['choices']
        ])
        return super().form_valid(form)


class DynamicModelSetUpdateView(LoginRequiredMixin, DynamicModelMixin, FormView):
    template_name = "crud/generic_update_view.html"
    context_object_name = 'all_objects'
    object = None

    def get_form_class(self):
        return get_dynamic_model_choice_set_form(self.dynamic_model)

    def get_initial(self):
        self.object = get_object_or_404(ModelSet, pk=self.kwargs.get('id'))
        return {
            'set': self.object,
            'choices': self.dynamic_model.objects.filter(sets__set=self.object)
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'remove_set': True,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(ModelSet, pk=self.kwargs.get('id'))
        return context

    def get_success_url(self):
        return reverse('database:set_crud', kwargs={'model': self.dynamic_model_name})

    def form_valid(self, form):
        SetMembership.objects.filter(
            set=form.cleaned_data['set'], content_type__model=self.dynamic_model.__name__.lower()
        ).delete()
        SetMembership.objects.bulk_create([
            SetMembership(
                set=form.cleaned_data['set'],
                member_object=choice
            )
            for choice in form.cleaned_data['choices']
        ])
        return super().form_valid(form)


class DynamicModelSetInspectView(LoginRequiredMixin, DynamicModelMixin, TemplateView):
    template_name = "crud/generic_inspection_view.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data_(*args, **kwargs)
        return self.render_to_response(context)

    def get_context_data_(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        objects = SetMembership.objects.filter(set__id=args[1]['id'],
                                               content_type__model=self.dynamic_model.__name__.lower())
        objs = []
        for obj in objects:
            objs.append(obj.member_object)
        context['field_data'] = serialize("python", objs, use_natural_foreign_keys=True)
        context['object'] = f"{ModelSet.objects.get(id=args[1]['id'])} - {self.dynamic_model.__name__}s"
        return context


class DynamicModelSetDeleteView(LoginRequiredMixin, DynamicModelMixin, DeleteView):
    template_name = "crud/generic_delete_view.html"

    def get_object(self):
        return ModelSet.objects.get(id=self.kwargs.get('id'))

    def delete(self, request, *args, **kwargs):
        SetMembership.objects.filter(
            set=self.get_object(), content_type__model=self.dynamic_model.__name__.lower()
        ).delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('database:set_crud', kwargs={'model': self.dynamic_model_name})
