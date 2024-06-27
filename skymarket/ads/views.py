from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from serializers import AdSerializer, CommentSerializer, AdDetailSerializer
from models import Ad, Comment
from permissions import IsAdmin, IsOwner
from paginators import AdPagination
from skymarket.ads.filters import AdFilter


class AdCreateAPIView(generics.CreateAPIView):
    serializer_class = AdDetailSerializer
    queryset = Ad.objects.all()
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdListAPIView(generics.ListAPIView):
    serializer_class = AdSerializer
    permission_classes = (AllowAny, )
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter

    def get_queryset(self):
        if self.action == "my_ads":
            return Ad.objects.filter(author=self.request.user).all()
        return Ad.objects.all()

    @action(
        detail=False,
        methods=[
            "get",
        ],
    )
    def my_ads(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class AdRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = AdDetailSerializer
    queryset = Ad.objects.all()
    permission_classes = (AllowAny, )


class AdUpdateAPIView(generics.UpdateAPIView):
    serializer_class = AdDetailSerializer
    queryset = Ad.objects.all()
    permission_classes = (IsOwner | IsAdmin, )


class AdDestroyAPIView(generics.DestroyAPIView):
    queryset = Ad.objects.all()
    permission_classes = (IsOwner | IsAdmin, )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        ad_id = self.kwargs.get("ad_pk")
        ad_instance = get_object_or_404(Ad, id=ad_id)
        user = self.request.user
        serializer.save(author=user, ad=ad_instance)

    def get_queryset(self):
        ad_id = self.kwargs.get("ad_pk")
        ad_instance = get_object_or_404(Ad, id=ad_id)
        return ad_instance.comments.all()

    def get_permissions(self):
        permission_classes = (IsAuthenticated,)
        if self.action in ["list", "retrieve"]:
            permission_classes = (IsAuthenticated,)
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = (IsOwner | IsAdmin,)
        return tuple(permission() for permission in permission_classes)

