from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, mixins
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Review, Category, Genre, Title
from users.models import User
from .filters import TitleFilter
from .permissions import AuthorOrReadOnly, IsAdminOrReadOnly, IsAdmin
from .serializers import (
    UserSerializer,
    UserAdminSerializer,
    ConfirmCodeSerializer,
    SignUpSerializer,
    CommentSerializer,
    ReviewSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleCreateSerializer,
    TitleSerializer,
)

ban_names = (
    'me',
    'Me',
    'Voldemort'
)


@api_view(['POST'])
def signup(request):
    """Функция регистрации нового пользователя
    отправляет confirmation_code на указанный email
    Запрещает использовать имя пользователя из кортежа ban_names"""

    serializer_data = SignUpSerializer(data=request.data)
    serializer_data.is_valid(raise_exception=True)
    email = serializer_data.data.get('email')
    username = serializer_data.data.get('username')
    if username in ban_names:
        return Response(
            'Выберите другое имя пользователя!',
            status=status.HTTP_400_BAD_REQUEST
        )
    new_user, create = User.objects.get_or_create(
        username=username,
        email=email,
    )
    confirmation_code = default_token_generator.make_token(new_user)
    print(confirmation_code)
    send_mail(
        'Youre registration is Done',
        f'Ваш код подтверждения (confirmation_code) {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    return Response({
        "email": email,
        "username": username
    })


@api_view(['POST'])
def give_token(request):
    """Выдает токен указаному пользователю, который прислал confirmation_code
    Вылсанный ранее на почту"""

    serializer_data = ConfirmCodeSerializer(data=request.data)
    serializer_data.is_valid(raise_exception=True)
    confirmation_code = serializer_data.data.get('confirmation_code')
    username = serializer_data.data.get('username')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return Response({
            "token": f"{token}"
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Изменение данных пользователям им самим"""

    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, partial=True, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для отзывов к произведению.

    Возваращает список всех отзывов, отзыв по id,
    может добавить обновить и удалить отзыв по id
    """
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        """Получаем набор отзывов относящихся к определенному произведению"""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        """При создании нового отзыва, автор = пользователь создающий отзыв"""
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для комментов к отзыву.

    Возваращает список всех комментов к отзыву, коммент по id,
    может добавить, обновить и удалить коммент по id
    """
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        """Получаем набор комментов относящихся к определенному отзыву"""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        """При создании нового коммента,
        автор = пользователь создающий коммент,
        отзыв = отзыв с необходимым id
        """
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """ Представление для категорий """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=name', )
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """ Представление для жанров """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """ Представление для произведений """
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleCreateSerializer
