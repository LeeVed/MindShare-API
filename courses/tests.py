from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson, Subscription
from users.models import CustomUser


class LessonTestCase(APITestCase):
    """Тестирование CRUD для уроков"""

    def setUp(self):
        """Создаем тестовые данные"""

        self.moderator_group = Group.objects.create(name="moderators")

        self.owner_user = CustomUser.objects.create_user(
            email="owner@test.com", password="testpass123", is_active=True
        )

        self.moderator_user = CustomUser.objects.create_user(
            email="moderator@test.com", password="testpass123", is_active=True
        )
        self.moderator_user.groups.add(self.moderator_group)

        self.other_user = CustomUser.objects.create_user(
            email="other@test.com", password="testpass123", is_active=True
        )

        self.course = Course.objects.create(
            name="Тестовый курс",
            description="Описание тестового курса",
            owner=self.owner_user,
        )

        self.lesson = Lesson.objects.create(
            name="Тестовый урок",
            description="Описание тестового урока",
            video_link="https://youtube.com/watch?v=123",
            course=self.course,
            owner=self.owner_user,
        )

        self.lesson_list_url = "/courses/lessons/"
        self.lesson_detail_url = f"/courses/lessons/{self.lesson.id}/"

    def test_lesson_create_authenticated(self):
        """Тест создания урока авторизованным пользователем"""

        self.client.force_authenticate(user=self.owner_user)

        data = {
            "name": "Новый урок",
            "description": "Описание нового урока",
            "video_link": "https://youtube.com/watch?v=456",
            "course": self.course.id,
        }

        response = self.client.post(self.lesson_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.last().owner, self.owner_user)

    def test_lesson_create_unauthenticated(self):
        """Тест создания урока неавторизованным пользователем"""

        data = {
            "name": "Новый урок",
            "description": "Описание нового урока",
            "video_link": "https://youtube.com/watch?v=456",
            "course": self.course.id,
        }

        response = self.client.post(self.lesson_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_create_moderator(self):
        """Тест создания урока модератором (запрещено)"""

        self.client.force_authenticate(user=self.moderator_user)

        data = {
            "name": "Новый урок",
            "description": "Описание нового урока",
            "video_link": "https://youtube.com/watch?v=456",
            "course": self.course.id,
        }

        response = self.client.post(self.lesson_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_list_authenticated(self):
        """Тест получения списка уроков авторизованным пользователем"""

        self.client.force_authenticate(user=self.owner_user)

        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_lesson_retrieve_owner(self):
        """Тест получения конкретного урока владельцем"""

        self.client.force_authenticate(user=self.owner_user)

        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.lesson.name)

    def test_lesson_update_owner(self):
        """Тест обновления урока владельцем"""

        self.client.force_authenticate(user=self.owner_user)

        data = {"name": "Обновленное название"}
        response = self.client.patch(self.lesson_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Обновленное название")

    def test_lesson_update_moderator(self):
        """Тест обновления урока модератором (разрешено)"""

        self.client.force_authenticate(user=self.moderator_user)

        data = {"name": "Обновлено модератором"}
        response = self.client.patch(self.lesson_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Обновлено модератором")

    def test_lesson_update_other_user(self):
        """Тест обновления урока другим пользователем (запрещено)"""

        self.client.force_authenticate(user=self.other_user)

        data = {"name": "Попытка взлома"}
        response = self.client.patch(self.lesson_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_owner(self):
        """Тест удаления урока владельцем"""

        self.client.force_authenticate(user=self.owner_user)

        response = self.client.delete(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_delete_moderator(self):
        """Тест удаления урока модератором (запрещено)"""

        self.client.force_authenticate(user=self.moderator_user)

        response = self.client.delete(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_other_user(self):
        """Тест удаления урока другим пользователем (запрещено)"""

        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_invalid_video_link(self):
        """Тест валидации ссылки на видео (только youtube)"""

        self.client.force_authenticate(user=self.owner_user)

        data = {
            "name": "Урок с плохой ссылкой",
            "video_link": "https://vimeo.com/123",
            "course": self.course.id,
        }

        response = self.client.post(self.lesson_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubscriptionTestCase(APITestCase):
    """Тестирование функционала подписок"""

    def setUp(self):
        """Создаем тестовые данные"""

        self.user1 = CustomUser.objects.create_user(
            email="user1@test.com", password="testpass123", is_active=True
        )

        self.user2 = CustomUser.objects.create_user(
            email="user2@test.com", password="testpass123", is_active=True
        )

        self.course = Course.objects.create(
            name="Тестовый курс для подписок", description="Описание", owner=self.user1
        )

        self.subscription_url = "/courses/subscriptions/"

    def test_subscribe_to_course(self):
        """Тест подписки на курс"""

        self.client.force_authenticate(user=self.user2)

        data = {"course_id": self.course.id}
        response = self.client.post(self.subscription_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user2, course=self.course).exists()
        )

    def test_unsubscribe_from_course(self):
        """Тест отписки от курса"""

        Subscription.objects.create(user=self.user2, course=self.course)

        self.client.force_authenticate(user=self.user2)
        data = {"course_id": self.course.id}
        response = self.client.post(self.subscription_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user2, course=self.course).exists()
        )

    def test_subscribe_unauthenticated(self):
        """Тест подписки неавторизованным пользователем"""

        data = {"course_id": self.course.id}
        response = self.client.post(self.subscription_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_nonexistent_course(self):
        """Тест подписки на несуществующий курс"""

        self.client.force_authenticate(user=self.user2)

        data = {"course_id": 999}
        response = self.client.post(self.subscription_url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_course_detail_with_subscription_status(self):
        """Тест наличия признака подписки при получении курса"""

        self.client.force_authenticate(user=self.user1)

        Subscription.objects.create(user=self.user1, course=self.course)

        url = f"/courses/courses/{self.course.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_subscribed", response.data)
        self.assertTrue(response.data["is_subscribed"])


class CoursePermissionsTestCase(APITestCase):
    """Тестирование прав доступа для курсов"""

    def setUp(self):

        self.moderator_group = Group.objects.create(name="moderators")

        self.owner_user = CustomUser.objects.create_user(
            email="owner@test.com", password="testpass123", is_active=True
        )

        self.moderator_user = CustomUser.objects.create_user(
            email="moderator@test.com", password="testpass123", is_active=True
        )
        self.moderator_user.groups.add(self.moderator_group)

        self.other_user = CustomUser.objects.create_user(
            email="other@test.com", password="testpass123", is_active=True
        )

        self.course = Course.objects.create(
            name="Тестовый курс", description="Описание", owner=self.owner_user
        )

        self.course_list_url = "/courses/courses/"
        self.course_detail_url = f"/courses/courses/{self.course.id}/"

    def test_course_list_for_owner(self):
        """Тест: владелец видит только свои курсы"""

        Course.objects.create(name="Чужой курс", owner=self.other_user)

        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.course_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 1)

    def test_course_list_for_moderator(self):
        """Тест: модератор видит все курсы"""

        Course.objects.create(name="Чужой курс", owner=self.other_user)

        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.get(self.course_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 2)
