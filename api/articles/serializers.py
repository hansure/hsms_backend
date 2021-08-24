from rest_framework import serializers
from .models import Article
# from accounts.models import UserAccount
# from rest_framework.authtoken.views import Token

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title','description']


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserAccount
#         fields = ['id','username','password']

#         extra_kwargs = {'password':{
#             'write_only':True,
#             'required':True
#         }}
#     def create(self, validated_data):
#         user = UserAccount.objects.create_user(**validated_data)
#         Token.objects.create(user=user)
#         return user