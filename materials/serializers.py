from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class LessonDetailSerializer(ModelSerializer):
    count_lesson_as_course = SerializerMethodField()

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

class CourseSerializer(ModelSerializer):
    lessons = LessonDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

