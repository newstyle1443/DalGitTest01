from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from users.serializers import UserSerializer,CustomTokenObtainPairSerializer,UserProrileSerializer
from users.models import User
from django.contrib import auth 
from rest_framework import status, permissions  # permission_classes 사용
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create your views here.

# ============================ 회원가입 클래스 (id,인증 불필요) ============================  
class UserView(APIView):
    # 회원가입
    def post(self, request):  # => request.method == 'POST':
        serializer = UserSerializer(data=request.data)  # 데이터 받아오기
        if serializer.is_valid():  # 유효성 검사 통과
            serializer.save()  # 받아온 데이터 db에 저장
            return Response(
                {"message": "가입완료!"}, status=status.HTTP_201_CREATED)  # 정상 생성 (등록) 상태
        else:  # 유효성 검사 만족 X -> 입력값에 문제
            return Response(
                {"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
            )  # 에러를 반환, 잘못된 요청 상태


# ============================ 로그인 ============================  
class CustomTokenObtainPairView(TokenObtainPairView):  # TokenObtainPairView 상속
    serializer_class = CustomTokenObtainPairSerializer

#유저프로필
class ProfileView(APIView):
    #프로필 보기
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserProrileSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"권한이 없습니다!"},status=status.HTTP_400_BAD_REQUEST)
    
    #프로필 수정 (2차)
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"권한이 없습니다!"},status=status.HTTP_400_BAD_REQUEST)
            
    #회원탈퇴
    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserSerializer(user, data=request.data)
            user.delete()
            return Response({"회원탈퇴 완료!"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"권한이 없습니다"},status=status.HTTP_403)



