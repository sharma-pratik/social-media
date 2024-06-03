from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import FriendRequest, AppUser


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = AppUser
        fields = ['email', 'first_name', 'last_name', 'password']
    
    def create(self, validated_data):
        user = AppUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid login credentials or Inactive user")


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id']

class FriendRequestCreateSerializer(serializers.ModelSerializer):
    from_user = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())
    to_user = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user']

    def validate(self, data):
        if FriendRequest.has_pending_request(from_user=data['from_user'], to_user=data['to_user']):
            raise serializers.ValidationError("A friend request already exists.")
        return data
    
    def create(self, validated_data):
        friend_request = FriendRequest.objects.create(
            from_user=validated_data['from_user'],
            to_user=validated_data['to_user']
        )
        return friend_request

class FriendRequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ['id', 'status']

    def validate(self, data):
        instance = self.instance
        if not FriendRequest.has_pending_request(from_user=instance.from_user, to_user=instance.to_user):
            raise serializers.ValidationError('Friend request can not be updated')
        return data

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = AppUserSerializer(read_only=True)
    to_user = AppUserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']


class SearchAppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'email', 'first_name', 'last_name']