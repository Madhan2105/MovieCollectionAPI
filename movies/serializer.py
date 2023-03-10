from rest_framework import serializers
from .models import Collection as CollectionModel
from django.contrib.auth.models import User as UserModel
from rest_framework_simplejwt.tokens import RefreshToken


class CollectionSerializer(serializers.ModelSerializer):
    collection_user = serializers.PrimaryKeyRelatedField(
                        queryset=UserModel.objects.all(), required=False)
    created_by = serializers.IntegerField(required=False)
    updated_by = serializers.IntegerField(required=False)
    favourite_genres = serializers.SerializerMethodField()

    def to_representation(self, obj):
        ret = super(CollectionSerializer, self).to_representation(obj)
        if self.context.get('show_only_collection_id', None):
            return {"collection_uuid": ret['id']}
        elif self.context.get('show_fav_genres', None):
            return ret
        else:
            ret.pop('favourite_genres')
            return ret

    def create(self, validated_data):
        user_data = CollectionModel(**validated_data)
        user_data.save()
        return user_data

    def get_favourite_genres(self, obj):
        hashmap = {}
        for movie in obj.movies:
            for genre in movie['genres'].split(","):
                if genre in hashmap:
                    hashmap[genre] += 1
                else:
                    hashmap[genre] = 1
        hashmap = sorted(hashmap.items(), key=lambda x: x[1], reverse=True)
        return [genre[0] for count, genre in enumerate(hashmap) if count < 3]

    class Meta:
        model = CollectionModel
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ['access_token', 'password', 'username']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True}
        }

    def get_access_token(self, obj):
        user = UserModel.objects.get(username=obj.username)
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def create(self, validated_data):
        user_data = UserModel(**validated_data)
        user_data.save()
        return user_data
