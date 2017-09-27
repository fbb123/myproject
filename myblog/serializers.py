from rest_framework import serializers
from .models import Category,Tag,Post

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','created')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name','created')
class PostSerializer(serializers.ModelSerializer):
    # category = serializers.CharField(source='category.name')
    content = {'content': {'write_only': True}}
    tags = TagSerializer(many=True)
    class Meta:
        model = Post
        fields = ('id','category','title','content','tags','created')