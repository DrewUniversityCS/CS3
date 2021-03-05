from django.urls import path

from database.views import department_crud, room_crud, building_crud, student_crud, teacher_crud, course_crud, \
    section_crud, schedule_crud, timeblock_crud, course_preference_crud, overlap_preference_crud, room_preference_crud, \
    timeblock_preference_crud, registration_crud

urlpatterns = [
    # User Models
    path('crud/students', student_crud),
    path('crud/teachers', teacher_crud),
    # Structural Models
    path('crud/departments', department_crud),
    path('crud/rooms', room_crud),
    path('crud/buildings', building_crud),
    # Schedule Models
    path('crud/courses', course_crud),
    path('crud/sections', section_crud),
    path('crud/schedules', schedule_crud),
    path('crud/timeblocks', timeblock_crud),
    # Relationships
    path('crud/course-preferences', course_preference_crud),
    path('crud/overlap-preferences', overlap_preference_crud),
    path('crud/room-preferences', room_preference_crud),
    path('crud/timeblock-preferences', timeblock_preference_crud),
    path('crud/registrations', registration_crud),
]

app_name = 'database'
