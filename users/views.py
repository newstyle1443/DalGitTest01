from rest_framework import status, permissions  # permission_classes 사용
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

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
