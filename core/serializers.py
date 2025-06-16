from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    User, TeacherProfile, ParentProfile, StudentProfile, 
    Class, Subject, Grade, Lesson)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user_type = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username,
                'user_type': user.user_type,
                'full_name': user.get_full_name(),
            }

            return validation
        except Exception as e:
            raise serializers.ValidationError(str(e))

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'user_type', 'phone', 'address']
        extra_kwargs = {
            'password': {'write_only': True},
            'user_type': {'read_only': True}
        }

class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = TeacherProfile
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(user_type='teacher', **user_data)
        return TeacherProfile.objects.create(user=user, **validated_data)

class ParentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = ParentProfile
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(user_type='parent', **user_data)
        return ParentProfile.objects.create(user=user, **validated_data)


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    parent = serializers.PrimaryKeyRelatedField(queryset=ParentProfile.objects.all())
    student_class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    
    class Meta:
        model = StudentProfile
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(user_type='student', **user_data)
        return StudentProfile.objects.create(user=user, **validated_data)
    

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    grade = GradeSerializer(read_only=True)
    grade_id = serializers.PrimaryKeyRelatedField(
        queryset=Grade.objects.all(), 
        source='grade', 
        write_only=True
    )
    supervisor = TeacherProfileSerializer(read_only=True)
    supervisor_id = serializers.PrimaryKeyRelatedField(
        queryset=TeacherProfile.objects.all(),
        source='supervisor',
        write_only=True
    )
    
    class Meta:
        model = Class
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subject',
        write_only=True
    )
    teacher = TeacherProfileSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=TeacherProfile.objects.all(),
        source='teacher',
        write_only=True
    )
    student_class = ClassSerializer(read_only=True)
    student_class_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        source='student_class',
        write_only=True
    )
    
    class Meta:
        model = Lesson
        fields = '__all__'