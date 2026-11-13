from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Genre, Artist, Album, CollectionItem
from .serializers import (
    RegisterSerializer,
    GenreSerializer,
    ArtistSerializer,
    AlbumSerializer,
    CollectionItemSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.select_related('artist', 'genre').all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]


class CollectionItemViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CollectionItem.objects.select_related('album', 'album__artist').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
