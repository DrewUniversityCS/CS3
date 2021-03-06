from django.urls import path

from database.views import CrudView, CrudDeleteView

urlpatterns = [
    # User Models
    path('crud/<slug:model>/', CrudView.as_view(), name='crud_model'),
    path('crud-delete/<slug:model>/<slug:id>/', CrudDeleteView.as_view(), name='crud_delete'),
    # path('crud/students', student_crud),
    # path('crud/teachers', teacher_crud),
    # # Structural Models
    # path('crud/departments', department_crud),
    # path('crud/rooms', room_crud),
    # path('crud/buildings', building_crud),
    # # Schedule Models
    # path('crud/courses', course_crud),
    # path('crud/sections', section_crud),
    # path('crud/schedules', schedule_crud),
    # path('crud/timeblocks', timeblock_crud),
    # # Relationships
    # path('crud/course-preferences', course_preference_crud),
    # path('crud/overlap-preferences', overlap_preference_crud),
    # path('crud/room-preferences', room_preference_crud),
    # path('crud/timeblock-preferences', timeblock_preference_crud),
    # path('crud/registrations', registration_crud),
]

app_name = 'database'
