def check_user_timeblock_preference(section, preferences, sections_dict):
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


def check_user_course_preference(section, preferences, sections_dict):
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


def check_user_section_preference(section, preferences, sections_dict):
    for preference in preferences:
        if preference.object_2 == section:
            color = sections_dict[section.id].get('color')
            if preference.weight:
                if section.primary_instructor.user == preference.object_1:
                    # If the preference is positive, and the section is taught by the specified teacher, highlight
                    # it green.
                    if color != 'red':
                        sections_dict[section.id]['color'] = 'green'
                    sections_dict[section.id]['positive_points'].append(
                        'Preference is positive, and the section is taught by the specified teacher'
                    )
                else:
                    # If the preference is positive, and the course is not taught by the specified teacher,
                    # highlight it red.
                    sections_dict[section.id]['color'] = 'red'
                    sections_dict[section.id]['negative_points'].append(
                        'The section is not taught by the specified teacher'
                    )
            else:
                # If the preference is negative, and the section is taught by the specified teacher, highlight it
                # red.
                if section.primary_instructor.user == preference.object_1:
                    sections_dict[section.id]['color'] = 'red'
                    sections_dict[section.id]['negative_points'].append(
                        'The preference is negative, and the section is taught by the specified teacher'
                    )


def check_section_timeblock_preference(section, preferences, sections_dict):
    for preference in preferences:
        if preference.object_1 == section:
            color = sections_dict[section.id].get('color')
            if preference.weight:
                if section.timeblock == preference.object_2:
                    # If the preference is positive, and the section is at the specified timeblock, highlight it
                    # green.
                    if color != 'red':
                        sections_dict[section.id]['color'] = 'green'
                    sections_dict[section.id]['positive_points'].append(
                        'Preference is positive, and the section is at the specified timeblock'
                    )
                else:
                    # If the preference is positive, and the section is not at the specified timeblock, highlight
                    # it red.
                    sections_dict[section.id]['color'] = 'red'
                    sections_dict[section.id]['negative_points'].append(
                        'The section is not at the specified timeblock'
                    )
            else:
                # If the preference is negative, and the section is at the specified timeblock, highlight it red.
                if section.timeblock == preference.object_2:
                    sections_dict[section.id]['color'] = 'red'
                    sections_dict[section.id]['negative_points'].append(
                        'Preference is negative, and the section is at the specified timeblock'
                    )
