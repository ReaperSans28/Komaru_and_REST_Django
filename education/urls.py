from django.urls import path
from rest_framework.routers import SimpleRouter

from education.views import CourseViewSet, LessonCreateApiView, LessonUpdateApiView, LessonRetrieveApiView, \
    LessonDestroyApiView, LessonListApiView
from education.apps import EducationConfig

app_name = EducationConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"),
    path("lessons/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lessons_delete"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
]

urlpatterns += router.urls
