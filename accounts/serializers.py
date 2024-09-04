from rest_framework import serializers
from django.contrib.auth.models import User

# 사용자 정보를 위한 커스텀 직렬화기 정의
class UserInfoSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    nickname = serializers.CharField(source='userprofile.nickname') 
    
    class Meta:
        model = User
        fields = ['username', 'nickname', 'roles']
    
    def get_roles(self, obj):
        return [{"role": "USER"}]