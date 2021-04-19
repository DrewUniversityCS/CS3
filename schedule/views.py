from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from database.models.schedule_models import Section, Timeblock
from database.models.structural_models import Preference
from schedule.forms import CheckScheduleForm, ScheduleSectionEditForm


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
        course_timeblock_preference = []
        user_course_preference = []
        user_timeblock_preference = []

        for preference in preferences:
            if preference.object_1_content_type.model == 'course':
                if preference.object_2_content_type.model == 'course':
                    course_course_preference.append(preference)
                elif preference.object_2_content_type.model == 'timeblock':
                    course_timeblock_preference.append(preference)
            elif preference.object_1_content_type.model == 'baseuser':
                if preference.object_2_content_type.model == 'course':
                    user_course_preference.append(preference)
                elif preference.object_2_content_type.model == 'timeblock':
                    user_timeblock_preference.append(preference)

        sections_dict = {}

        section_time_block_dict = defaultdict(list)
        for section in sections:
            section_time_block_dict[section.timeblock.id].append(section)
            sections_dict[section.id] = {
                'section': section,
                'section_edit_form': ScheduleSectionEditForm(instance=section),
                'color': '',
                'positive_points': [],
                'negative_points': []
            }

        for idx, section1 in enumerate(sections):
            for section2 in sections[idx:]:
                for preference in course_course_preference:
                    preference_courses = [preference.object_1, preference.object_2]
                    section_courses = [section1.course, section2.course]
                    if preference_courses == section_courses:
                        color1 = sections_dict[section1.id].get('color')
                        color2 = sections_dict[section2.id].get('color')
                        print(preference)
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

            self.check_course_timeblock_preference(section1, course_timeblock_preference, sections_dict)
            self.check_user_course_preference(section1, user_course_preference, sections_dict)
            self.check_user_timeblock_preference(section1, user_timeblock_preference, sections_dict)

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
            'preference_set_id': kwargs.get('preference_set_id')
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

    def check_course_timeblock_preference(self, section, preferences, sections_dict):
        for preference in preferences:
            if preference.object_1 == section.course:
                color = sections_dict[section.id].get('color')
                if preference.weight:
                    if section.timeblock == preference.object_2:
                        # If the preference is positive, and the course is at the specified timeblock, highlight it
                        # green.
                        if color != 'red':
                            sections_dict[section.id]['color'] = 'green'
                        sections_dict[section.id]['positive_points'].append(
                            'preference is positive, and the course is at the specified timeblock'
                        )
                    else:
                        # If the preference is positive, and the course is not at the specified timeblock, highlight
                        # it red.
                        sections_dict[section.id]['color'] = 'red'
                        sections_dict[section.id]['negative_points'].append(
                            'the course is not at the specified timeblock'
                        )
                else:
                    # If the preference is negative, and the course is at the specified timeblock, highlight it red.
                    if section.timeblock == preference.object_2:
                        sections_dict[section.id]['color'] = 'red'
                        sections_dict[section.id]['negative_points'].append(
                            'preference is negative, and the course is at the specified timeblock'
                        )

    def check_user_course_preference(self, section, preferences, sections_dict):
        for preference in preferences:
            if preference.object_2 == section.course:
                color = sections_dict[section.id].get('color')
                if preference.weight:
                    if section.primary_instructor.user == preference.object_1:
                        # If the preference is positive, and the course is taught by the specified teacher, highlight
                        # it green.
                        if color != 'red':
                            sections_dict[section.id]['color'] = 'green'
                        sections_dict[section.id]['positive_points'].append(
                            'preference is positive, and the course is taught by the specified teacher'
                        )
                    else:
                        # If the preference is positive, and the course is not taught by the specified teacher,
                        # highlight it red.
                        sections_dict[section.id]['color'] = 'red'
                        sections_dict[section.id]['negative_points'].append(
                            'the course is not taught by the specified teacher'
                        )
                else:
                    # If the preference is negative, and the course is taught by the specified teacher, highlight it
                    # red.
                    if section.primary_instructor.user == preference.object_1:
                        sections_dict[section.id]['color'] = 'red'
                        sections_dict[section.id]['negative_points'].append(
                            'the preference is negative, and the course is taught by the specified teacher'
                        )

    def check_user_timeblock_preference(self, section, preferences, sections_dict):
        for preference in preferences:
            if preference.object_1 == section.primary_instructor.user:
                color = sections_dict[section.id].get('color')
                if preference.weight:
                    if section.timeblock == preference.object_2:
                        # If the preference is positive, and the specified teacher is teaching a class during the
                        # specified timeblock, highlight the section green.
                        if color != 'red':
                            sections_dict[section.id]['color'] = 'green'
                        sections_dict[section.id]['positive_points'].append(
                            'The specified teacher is teaching a class during the specified timeblock'
                        )
                    else:
                        # If the preference is positive, and the specified teacher is not teaching a class during the
                        # specified timeblock, highlight it red.
                        sections_dict[section.id]['color'] = 'red'
                        sections_dict[section.id]['negative_points'].append(
                            'specified teacher is not teaching a class during the specified timeblock'
                        )
                else:
                    # If the preference is negative, and the specified teacher is teaching a class during the
                    # specified timeblock, highlight the section red.
                    if section.timeblock == preference.object_2:
                        sections_dict[section.id]['color'] = 'red'
                        sections_dict[section.id]['negative_points'].append(
                            'preference is negative, and the specified teacher is teaching a class during the '
                            'specified timeblock '
                        )


class ScheduleSectionEditView(LoginRequiredMixin, FormView):

    def get_form(self, form_class=None):
        return ScheduleSectionEditForm(
            instance=Section.objects.get(id=self.kwargs['section_id']), **self.get_form_kwargs()
        )

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse(
            'schedule:schedule-table-view',
            kwargs={
                'schedule_id': self.kwargs['schedule_id'],
                'preference_set_id': self.kwargs['preference_set_id']
            }
        ))
