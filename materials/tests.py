from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from materials.models import Lesson, Course


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="Курс 1")
        self.lesson = Lesson.objects.create(name="Введение", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        '''сравниваем статус код'''
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''сравниваем название урока'''
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("materials:lesson-list")
        data = {"name": "Начало"}
        response = self.client.post(url, data)
#       print(response.data)
        '''сравниваем статус код'''
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        '''сравниваем количество уроков'''
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        data = {"name": "Начало"}
        response = self.client.patch(url, data)
        data = response.json()
        '''сравниваем статус код'''
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''сравниваем обновленное название урока'''
        self.assertEqual(data.get("name"), "Начало")

    def test_lesson_delete(self):
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.delete(url)
        '''сравниваем статус код'''
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        '''сравниваем количество уроков после удаления'''
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {'id': self.lesson.pk,
                 'url': None,
                 'name': 'Введение',
                 'description': None,
                 'picture': None,
                 'video': None,
                 'course': self.course.pk,
                 'owner': self.user.pk}]}
        '''сравниваем статус код'''
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''сравниваем список уроков'''
        self.assertEqual(data, result)


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="Курс 1", owner=self.user)
        self.lesson = Lesson.objects.create(name="Введение", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:courses_retrieve", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        '''сравниваем статус код'''
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''сравниваем название курса'''
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        url = reverse("materials:courses_create")
        data = {"name": "Курс 2"}
        response = self.client.post(url, data)
#       print(response.data)
        '''сравниваем статус код'''
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        '''сравниваем количество курсов'''
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("materials:courses_update", args=(self.course.pk,))
        data = {"name": "Курс 3"}
        response = self.client.patch(url, data)
        data = response.json()
        '''сравниваем статус код'''
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''сравниваем обновленное название курса'''
        self.assertEqual(data.get("name"), "Курс 3")

    def test_course_delete(self):
        url = reverse("materials:courses_delete", args=(self.course.pk,))
        response = self.client.delete(url)
        '''сравниваем статус код'''
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        '''сравниваем количество курсов после удаления'''
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("materials:courses_list")
        response = self.client.get(url)
        data = response.json()
        print(data)
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {'id': self.course.pk,
                 'lessons': [self.lesson.name],
                 'name': self.course.name,
                 'description': self.course.description,
                 'owner': self.user.pk}]}
        '''сравниваем статус код'''
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''сравниваем список уроков'''
        self.assertEqual(data, result)
