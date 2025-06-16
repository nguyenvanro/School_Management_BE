from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from core.serializers import UserLoginSerializer
from core.models import (
    TeacherProfile, ParentProfile, StudentProfile,
    Grade, Subject, Class, Lesson)
from core.serializers import (TeacherProfileSerializer, ParentProfileSerializer, 
                              StudentProfileSerializer, GradeSerializer, SubjectSerializer, 
                              ClassSerializer, LessonSerializer)


class UserLoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_fields = ['qualification', 'subjects']


class ParentProfileViewSet(viewsets.ModelViewSet):
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'parent':
            return ParentProfile.objects.filter(user=self.request.user)
        return ParentProfile.objects.all()


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ['student_class', 'parent']
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'student':
            return StudentProfile.objects.filter(user=user)
        elif user.user_type == 'parent':
            return StudentProfile.objects.filter(parent__user=user)
        return StudentProfile.objects.all()
    

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ['grade', 'teachers']

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ['grade', 'supervisor', 'academic_year']
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'teacher':
            return Class.objects.filter(supervisor__user=user)
        return Class.objects.all()

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ['subject', 'teacher', 'student_class', 'date']
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'teacher':
            return Lesson.objects.filter(teacher__user=user)
        elif user.user_type == 'student':
            return Lesson.objects.filter(student_class=user.student_profile.student_class)
        return Lesson.objects.all()