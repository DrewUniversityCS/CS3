from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize, deserialize
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, resolve
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, DeleteView, UpdateView

from accounts.models import BaseUser
from database.forms import get_dynamic_model_form, get_dynamic_model_choice_set_form, CreateBulkSectionsForm, \
    EmptyForm, CreatePreferenceForm
from database.models.schedule_models import Course, Section, Schedule, Timeblock
from database.models.structural_models import Department, ModelSet, SetMembership, Preference
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


class CreateBulkSectionsView(LoginRequiredMixin, FormView):
    template_name = 'crud/sections_bulk_create.html'
    form_class = CreateBulkSectionsForm
    success_url = '/crud/create-bulk-sections/success'

    def form_valid(self, form):
        schedule = Schedule.objects.get(pk=form.data['schedule'])
        course_set = ModelSet.objects.get(pk=form.data['courses'])
        set_memberships = SetMembership.objects.filter(set=course_set)
        courses = Course.objects.filter(sets__in=set_memberships)

        sections = []
        for course in courses.iterator():
            section = Section.create(course, schedule)
            sections.append(section)

        # we save the sections in the request for later use
        self.request.session['sections'] = serialize('json', sections)

        return super().form_valid(form)


class CreateBulkSectionsSuccessView(LoginRequiredMixin, FormView):
    template_name = "crud/sections_bulk_create_success.html"
    form_class = EmptyForm
    success_url = "/crud/create-bulk-sections"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        sections = []
        for obj in deserialize("json", self.request.session.get('sections')):
            sections.append(obj.object)

        context['sections'] = sections
        return context

    def form_valid(self, form):
        if 'confirm' in self.request.POST:
            for obj in deserialize("json", self.request.session.get('sections')):
                obj.object.save()

        return redirect(self.success_url)


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
            if self.dynamic_model == Student:
                context['form'] = self.get_form_class()(
                    instance=self.object,
                    initial={
                        'first_name': user_object.first_name,
                        'last_name': user_object.last_name,
                        'email': user_object.email,
                        'student_id': self.object.student_id,
                        'class_standing': self.object.class_standing
                    })
            else:
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
        render_type = False
        render_form = True
        if self.dynamic_model_name == 'preferences':
            render_form = False
        elif self.dynamic_model_name == 'model-set':
            render_form = False
            render_type = True

        context.update({
            'render_form': render_form,
            'all_objects': self.dynamic_model.objects.all(),
            'dynamic_model_name': self.dynamic_model_name,
            'render_type': render_type
        })
        return context

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DynamicModelSetCreateView(LoginRequiredMixin, DynamicModelMixin, FormView):
    template_name = "crud/set_crud_view.html"
    context_object_name = 'all_objects'

    def get_form_class(self):
        return get_dynamic_model_choice_set_form(self.dynamic_model, "create")

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
        if form.cleaned_data['new_set_name'] != "":
            new_set = ModelSet.objects.create(name=form.cleaned_data['new_set_name'],
                                              obj_type=ContentType.objects.get(
                                                  model=self.dynamic_model.__name__.lower()))
            SetMembership.objects.bulk_create([
                SetMembership(
                    set=new_set,
                    member_object=choice
                )
                for choice in form.cleaned_data['choices']
            ])
        else:
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
        return get_dynamic_model_choice_set_form(self.dynamic_model, "update")

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
        ModelSet.objects.filter(id=self.kwargs.get('id')).delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('database:set_crud', kwargs={'model': self.dynamic_model_name})


class CreatePreferenceView(LoginRequiredMixin, FormView):
    template_name = 'crud/create_preference.html'
    form_class = CreatePreferenceForm
    success_url = '/crud/preferences'

    def form_valid(self, form):
        obj_1_id = form.cleaned_data['object_1'].id
        obj_1_ct = form.cleaned_data['object_1_type']
        obj_2_id = form.cleaned_data['object_2'].id
        obj_2_ct = form.cleaned_data['object_2_type']
        weight = form.cleaned_data['weight']

        Preference.objects.create(
            object_1_id=obj_1_id,
            object_1_content_type=obj_1_ct,
            object_2_id=obj_2_id,
            object_2_content_type=obj_2_ct,
            weight=weight
        ).save()
        return HttpResponseRedirect(self.get_success_url())
