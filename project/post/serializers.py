from rest_framework import serializers
from .models import *

# 시리얼라이저를 나누는 이유: 각각 시리얼라이저는 특정 메소드에 맞춰 필요한 필드와 데이터를 반환
# => API응답을 필요에 따라 조절해서 불필요 데이터를 제거하는 게 효율적인 통신을 돕는다
class PostSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True, required=False)
    comments = serializers.SerializerMethodField(read_only=True)

    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    
    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = [
            "id",
            "writer",
            "created_at",
            "updated_at",
            "comments", # 댓글 목록 불러오기
            "click_num",
            "likes"
        ]

class PostListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "writer",
            "created_at",
            "updated_at",
            "image",
            "comments_cnt", # 댓글 개수 불러옴
            "tag",
            "likes"
        ]
        read_only_fields = ["id", "creatd_at", "updated_at", "comments_cnt"]

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post']

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'