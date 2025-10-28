from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_forbidden_words


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.URLField(validators= [validate_forbidden_words])

    class Meta:
        model = Lesson
        fields = "__all__"

class LessonDetailSerializer(serializers.ModelSerializer):
    count_lesson_as_course = serializers.SerializerMethodField()

    def get_count_lesson_as_course(self, lesson):
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

    class Meta:
        model = Course
        fields = "__all__"
