from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Genre, Artist, Album, CollectionItem

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    artist_name = serializers.ReadOnlyField(source='artist.name')
    genre_name = serializers.ReadOnlyField(source='genre.name')

    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'artist_name', 'genre', 'genre_name', 'release_year', 'cover_url']


class CollectionItemSerializer(serializers.ModelSerializer):
    album_title = serializers.ReadOnlyField(source='album.title')
    artist_name = serializers.ReadOnlyField(source='album.artist.name')
    format_display = serializers.ReadOnlyField(source='get_format_display')
    condition_display = serializers.ReadOnlyField(source='get_condition_display')

    class Meta:
        model = CollectionItem
        fields = [
            'id', 'album', 'album_title', 'artist_name',
            'format', 'format_display', 'condition', 'condition_display',
            'notes', 'added_at'
        ]
        read_only_fields = ['id', 'added_at']
