import json

from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import FormView, TemplateView, CreateView

from database.models.schedule_models import Section, Timeblock, SectionNote
from database.models.structural_models import Preference
from schedule.forms import CheckScheduleForm, ScheduleSectionEditForm, SectionNoteForm
from schedule.functions import check_section_timeblock_preference, check_user_timeblock_preference, \
    check_user_course_preference, check_user_section_preference


class ScheduleRedirectView(LoginRequiredMixin, FormView):
    form_class = CheckScheduleForm

    def form_valid(self, form):
        return HttpResponseRedirect(
            reverse(
                'schedule:schedule-table-view',
                kwargs={
                    'schedule_id': form.cleaned_data['schedule'].id,
                    'preference_set_id': form.cleaned_data['preference_set'].id
                }
            )
        )


class CheckScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/check_schedule.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'check_schedule_form': CheckScheduleForm()
        })
        return context_data


class ScheduleView(LoginRequiredMixin, TemplateView):
    template_name = "pages/schedule_table_view.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        sections = Section.objects.filter(schedule_id=kwargs.get('schedule_id'))
        preferences = Preference.objects.filter(sets__set__id=kwargs.get('preference_set_id'))

        course_course_preference = []
        section_timeblock_preference = []
        user_course_preference = []
        user_section_preference = []
        user_timeblock_preference = []

        for preference in preferences:
            if preference.object_1_content_type.model == 'course':
                if preference.object_2_content_type.model == 'course':
                    course_course_preference.append(preference)
            if preference.object_1_content_type.model == 'section':
                if preference.object_2_content_type.model == 'timeblock':
                    section_timeblock_preference.append(preference)
            elif preference.object_1_content_type.model == 'baseuser':
                if preference.object_2_content_type.model == 'course':
                    user_course_preference.append(preference)
                elif preference.object_2_content_type.model == 'timeblock':
                    user_timeblock_preference.append(preference)
                elif preference.object_2_content_type.model == 'section':
                    user_section_preference.append(preference)

        sections_dict = {}
        sections_without_timeblock = []

        section_time_block_dict = defaultdict(list)
        for section in sections:
            if section.timeblock:
                section_time_block_dict[section.timeblock.id].append(section)
            else:
                sections_without_timeblock.append(section)
            sections_dict[section.id] = {
                'section': section,
                'color': '',
                'positive_points': [],
                'negative_points': []
            }

        i = 0
        new_list = []
        while i < len(sections_without_timeblock):
            new_list.append(sections_without_timeblock[i:i + 5])
            i += 5

        sections_without_timeblock = new_list

        for idx, section1 in enumerate(sections):
            for section2 in sections[idx:]:
                for preference in course_course_preference:
                    preference_courses = [preference.object_1, preference.object_2]
                    section_courses = [section1.course, section2.course]
                    if preference_courses == section_courses:
                        color1 = sections_dict[section1.id].get('color')
                        color2 = sections_dict[section2.id].get('color')
                        if preference.weight:
                            if section1.timeblock == section2.timeblock:
                                # If two courses with a positive preference are at the same time, highlight both green.
                                if color1 != 'red':
                                    sections_dict[section1.id]['color'] = 'green'
                                if color2 != 'red':
                                    sections_dict[section2.id]['color'] = 'green'
                                sections_dict[section1.id]['positive_points'].append(
                                    'courses with a positive preference are at the same time'
                                )
                                sections_dict[section2.id]['positive_points'].append(
                                    'courses with a positive preference are at the same time'
                                )
                            else:
                                # If two courses with a positive preference are at different times, highlight both red.
                                sections_dict[section1.id]['color'] = 'red'
                                sections_dict[section1.id]['negative_points'].append(
                                    'courses with a positive preference are at different times'
                                )
                                sections_dict[section2.id]['color'] = 'red'
                                sections_dict[section2.id]['negative_points'].append(
                                    'courses with a positive preference are at different times'
                                )
                        else:
                            # If two courses with a negative preference are at the same time, highlight both red.
                            if section1.timeblock == section2.timeblock:
                                sections_dict[section1.id]['color'] = 'red'
                                sections_dict[section1.id]['negative_points'].append(
                                    'courses with a negative preference are at the same time'
                                )
                                sections_dict[section2.id]['color'] = 'red'
                                sections_dict[section2.id]['negative_points'].append(
                                    'courses with a negative preference are at the same time'
                                )

            if section1.primary_instructor:
                check_user_course_preference(section1, user_course_preference, sections_dict)
                check_user_section_preference(section1, user_section_preference, sections_dict)

            if section1.timeblock:
                check_section_timeblock_preference(section1, section_timeblock_preference, sections_dict)

            if section1.timeblock and section1.primary_instructor:
                check_user_timeblock_preference(section1, user_timeblock_preference, sections_dict)

        timeblock_day_dict = defaultdict(dict)
        time_blocks = Timeblock.objects.all()

        for time_block in time_blocks:
            timeblock_day_dict[time_block.id] = self.generate_day_dict(section_time_block_dict[time_block.id])

        context_data.update({
            'time_blocks': time_blocks,
            'timeblock_day_dict': timeblock_day_dict,
            'day_list': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
            'sections': sections_dict,
            'schedule_id': kwargs.get('schedule_id'),
            'preference_set_id': kwargs.get('preference_set_id'),
            'sections_queryset': sections,
            'sections_without_timeblock': sections_without_timeblock
        })

        return context_data

    @classmethod
    def generate_day_dict(cls, sections):
        day_dict = defaultdict(list)
        for section in sections:
            if section.timeblock.weekdays.monday:
                day_dict['monday'].append(section)

            if section.timeblock.weekdays.tuesday:
                day_dict['tuesday'].append(section)

            if section.timeblock.weekdays.wednesday:
                day_dict['wednesday'].append(section)

            if section.timeblock.weekdays.thursday:
                day_dict['thursday'].append(section)

            if section.timeblock.weekdays.friday:
                day_dict['friday'].append(section)

        return day_dict


class ScheduleSectionEditView(LoginRequiredMixin, FormView):
    template_name = 'pages/section_edit_form.html'

    def get_form(self, form_class=None):
        return ScheduleSectionEditForm(
            instance=Section.objects.get(id=self.kwargs['section_id']), **self.get_form_kwargs()
        )

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(
            reverse(
                'schedule:schedule-table-view',
                kwargs={
                    'schedule_id': self.kwargs['schedule_id'],
                    'preference_set_id': self.kwargs['preference_set_id']
                }
            ) + f'?showsections={self.request.GET.get("showsections", "")}'
        )


class SectionNoteListView(LoginRequiredMixin, TemplateView):
    template_name = 'components/section_notes.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'notes': SectionNote.objects.filter(
                section__id=self.kwargs['section_id'],
                color='#' + self.kwargs['color']
            ),
            'color_type': '#' + self.kwargs['color']
        })
        return context_data


class SectionNoteFormView(LoginRequiredMixin, FormView):
    template_name = 'pages/section_edit_form.html'
    form_class = SectionNoteForm

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': json.loads(self.request.body),
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        note = form.save(commit=False)
        note.section = Section.objects.get(id=self.kwargs['section_id'])
        note.save()
        return HttpResponseRedirect(reverse(
            'schedule:section-notes-list',
            kwargs={
                'section_id': self.kwargs['section_id'],
                'color': form.cleaned_data['color'][1:]
            }
        ))


