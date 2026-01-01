from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'created_at', 'permissions']
    def get_permissions(self, user):
        return list(user.userpermission_set.values_list("permission__code", flat=True))

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Account already exists")
        return value


    def create(self, validated_data):
        return User.objects.create_user(email=validated_data['email'], password=validated_data['password'], name=validated_data['name'])