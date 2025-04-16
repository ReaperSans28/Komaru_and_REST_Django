from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group

from education.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.moderators_group, _ = Group.objects.get_or_create(name="moderators")
        self.user = User.objects.create(email="test@test.com", is_superuser=True)
        self.user.groups.add(self.moderators_group)
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(name="test", owner=self.user)

    def test_create_lesson(self):
        course = Course.objects.create(name="Test Course", owner=self.user)

        data = {"name": "test lesson", "course": course.pk}
        response = self.client.post("/lessons/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["name"], "test lesson")

    def test_create_lesson_failed(self):
        data = {"name": "", "video": "https://test.com/"}
        response = self.client.post("/lessons/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_lessons(self):
        response = self.client.get("/lessons/")
        response1 = self.client.get(f"/lessons/{self.lesson.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

    def test_view_lesson_failed(self):
        response = self.client.get("/lessons/0/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_lesson(self):
        data = {
            "name": "updated test lesson",
            "description": "updated description",
        }
        response = self.client.put(f"/lessons/{self.lesson.pk}/update/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "updated test lesson")
        self.assertEqual(response.json()["description"], "updated description")

    def test_delete_lesson(self):
        response = self.client.delete(f"/lessons/{self.lesson.pk}/delete/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_failed(self):
        response = self.client.delete("/lessons/0/delete/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SubTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name="test")

    def test_subscription(self):
        data = {"course_id": self.course.pk}
        response = self.client.post("/course/subscription/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {"message": "Подписка на урок/курс добавлена"}
        )

        response1 = self.client.post("/course/subscription/", data=data)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.json(), {"message": "Подписка на урок/курс удалена"})
