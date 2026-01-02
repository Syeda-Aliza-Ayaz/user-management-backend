# from .models import User
# from rest_framework import serializers

# # class UserSerializer(serializers.ModelSerializer):
# #     permissions = serializers.SerializerMethodField()
# #     class Meta:
# #         model = User
# #         fields = ['id', 'email', 'name', 'role', 'created_at', 'permissions']
# #     def get_permissions(self, user):
# #         return list(user.userpermission_set.values_list("permission__code", flat=True))
# class UserSerializer(serializers.ModelSerializer):
#     permissions = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ['id', 'email', 'name', 'role', 'created_at', 'permissions', 'department', 'purse_number']
#         # Add these two fields ↑
    
#     def get_permissions(self, user):
#         return list(user.userpermission_set.values_list("permission__code", flat=True))

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = User
#         fields = ['email', 'name', 'password']
#         extra_kwargs = {"password": {"write_only": True}}

#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("Account already exists")
#         return value


#     def create(self, validated_data):
#         return User.objects.create_user(email=validated_data['email'], password=validated_data['password'], name=validated_data['name'])
from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'role', 'created_at',
            'permissions', 'department', 'purse_number'
        ]

    def get_permissions(self, user):
        return list(user.userpermission_set.values_list("permission__code", flat=True))


# accounts/serializers.py

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'department', 'purse_number']
        extra_kwargs = {
            "password": {"write_only": True},
            "department": {"required": False, "allow_blank": True},
            "purse_number": {"required": False, "allow_blank": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Account already exists")
        return value

    def create(self, validated_data):
        # Safely extract optional fields
        department = validated_data.pop('department', '')
        purse_number = validated_data.pop('purse_number', '')

        # Create user with required fields
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            department=department,
            purse_number=purse_number,
        )
        return user