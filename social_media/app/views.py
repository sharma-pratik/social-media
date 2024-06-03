# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import AppUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q

class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'data' : {
                    'token': token.key,
                    'user': {
                        'email': user.email,
                        'name': f'{user.first_name} {user.last_name}',
                    }
                },
                'message': 'User created successfully',
                'status': 'success'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            print('user' , user)
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
            else:
                return Response({'error': 'User account is inactive'}, status=status.HTTP_403_FORBIDDEN)
            return Response({
                'data' : {
                    'token': token.key,
                    'user': {
                        'email': user.email
                    }
                },
                'message': 'User logged in successfully',
                'status': 'success'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendRequestCreateUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_throttles(self):
        from app.throttles import UserFriendRequestThrottle

        if self.request.method == 'POST':
            return [UserFriendRequestThrottle()]
        return super().get_throttles()


    def post(self, request, *args, **kwargs):
        serializer = FriendRequestCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        try:
            friend_request = FriendRequest.objects.get(id=kwargs['pk'], from_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FriendRequestUpdateSerializer(friend_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics

class ListFriendRequestListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status')
        serializer = FriendRequestSerializer(data={'status': status})
        serializer.is_valid(raise_exception=True)
        return FriendRequest.objects.filter(from_user=self.request.user, status=status)


class UserSearchView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SearchAppUserSerializer


    def get_queryset(self):
        query = self.request.query_params.get('search', '')
        if query:
            return AppUser.objects.exclude(id=self.request.user.id).filter(
                Q(email__iexact=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        return AppUser.objects.none()