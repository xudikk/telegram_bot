from rest_framework import serializers

class SignInSerializer(serializers.Serializer):
    username = serializers.EmailField(max_length=50, min_length=2, required=True, write_only=True,)
    password = serializers.CharField(required=True,  write_only=True, min_length=4, max_length=50,)


class RefreshTokenSerializer(serializers.Serializer):
    client_id = serializers.CharField(min_length=10, required=True,  write_only=True)
    refresh_token = serializers.CharField(min_length=10, required=True,  write_only=True)
    client_secret = serializers.CharField(required=True,  write_only=True)
    grant_type = serializers.CharField(required=True,  write_only=True)

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=10, required=True,  write_only=True)