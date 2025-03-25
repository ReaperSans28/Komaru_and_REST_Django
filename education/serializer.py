from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from education.models import Course, Lesson, Subscription
from education.validators import YouTubeValidator


class LessonDetailSerializer(ModelSerializer):
    count_lessons_with_same_course = SerializerMethodField()

    def get_count_lessons_with_same_course(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = ("name", "course", "count_lessons_with_same_course")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeValidator(field="video_url")]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "image", "lessons", "count_lessons", "subscription")

    def get_count_lessons(self, course):
        return course.lessons.count()

    def get_subscription(self, course):
        user = self.context['request'].user
        return Subscription.objects.all().filter(user=user).filter(course=course).exists()


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
