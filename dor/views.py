from dor.models import Repository, Taxonomy, Standards, ContentType, Journal
from dor.serializers import UserSerializer, RepositorySerializer, TaxonomySerializer, StandardsSerializer, ContentTypeSerializer, JournalSerializer
from dor.permissions import IsOwnerOrReadOnly, CanCreateOrReadOnly
from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'repos': reverse('repo-list', request=request, format=format)
    })

class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,
                          CanCreateOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer


class StandardsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Standards.objects.all()
    serializer_class = StandardsSerializer


class TaxonomyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer


class RepositoryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = [CanCreateOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,]

    def perform_create(self, serializer):
       serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
