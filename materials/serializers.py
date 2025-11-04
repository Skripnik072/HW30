from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_forbidden_words

from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.URLField(validators= [validate_forbidden_words], required=False, allow_blank=True)

    class Meta:
        model = Lesson
        fields = "__all__"

class LessonDetailSerializer(serializers.ModelSerializer):
    count_lesson_as_course = serializers.SerializerMethodField()

    def get_count_lesson_as_course(self, lesson):
        '''Подсчет количества уроков в курсе'''
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = (
            "name",
            "description",
            "course",
            "count_lesson_as_course",
        )

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonDetailSerializer(many=True, read_only=True)
    subscription = SerializerMethodField()

    def get_subscription(self, obj):
        '''Вызывает пользователя, передает информацию в контекст, проверяет наличие подписки на курс'''
        user = self.context['request'].user
        if Subscription.objects.filter(user=user, course=obj).exists():
            return True
        else:
            return False

    class Meta:
        model = Course
        fields = "__all__"
