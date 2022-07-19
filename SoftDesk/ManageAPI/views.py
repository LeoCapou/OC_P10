from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from ManageAPI.permissions import (
    DeleteModify_Issue_AuthorOnly,
    Access_Project,
    Access_Comment,
)


from django.shortcuts import get_object_or_404


from ManageAPI.serializers import (
    SignUpSerializer,
    ProjectsSerializer,
    ContributorsSerializer,
    IssuesSerializer,
    CommentsSerializer,
)
from ManageAPI.models import Contributors, Projects, Issues, Comments


class CommentsViewset(ModelViewSet):
    """
    COMMENTAIRE
    """

    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated & Access_Comment]

    def get_queryset(self):
        if "pk" in self.kwargs:
            return Comments.objects.filter(
                comment_id=self.kwargs["pk"]
            )  # unique comment
        else:
            return Comments.objects.filter(
                issue__id=self.kwargs["issue_pk"]
            )  # tous les comments d'une issue

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data.update(
                author_user=self.request.user.id,
                created_time=datetime.now(),
                comment_id=0,
                issue=kwargs["issue_pk"],
            )
            serializer = CommentsSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                comment = self.perform_create(serializer)
                comment = serializer.save()
                comment.comment_id = comment.id
                comment.save()
                return Response(
                    {"Message": "Un commentaire a été ajoutée à la issue."},
                    status=status.HTTP_200_OK,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"Message": "Quelque chose a échoué à cause de {}".format(str(e))},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(
            {"Message": "Le commentaire a été supprimé."}, status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        comment_serializer = CommentsSerializer(
            comment, data=request.data, partial=True
        )

        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(
                {"Message": "Comment a bien été modifié"}, status=status.HTTP_200_OK
            )

        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssuesViewset(ModelViewSet):
    """
    ISSUE
    """

    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated & DeleteModify_Issue_AuthorOnly]

    def get_queryset(self):
        return Issues.objects.filter(project=self.kwargs["project_pk"])

    def create(self, request, project_pk):
        try:
            data = request.data.copy()
            data.update(
                project=project_pk,
                author_user=self.request.user.id,
                created_time=datetime.now(),
            )
            serializer = IssuesSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
                serializer.save(project_id=project_pk)
                return Response(
                    {"Message": "Une issue a été ajoutée au projet."},
                    status=status.HTTP_200_OK,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"Message": "Quelque chose a échoué à cause de {}".format(str(e))},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        issue = self.get_object()
        issue_serializer = IssuesSerializer(issue, data=request.data, partial=True)

        if issue_serializer.is_valid():
            issue_serializer.save()
            return Response(
                {"Message": "Issue a bien été modifié"}, status=status.HTTP_200_OK
            )

        return Response(issue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        issue = self.get_object()
        issue.delete()
        return Response(
            {"Message": "Le problème a été supprimé du projet."},
            status=status.HTTP_200_OK,
        )


class ContributorsViewset(ModelViewSet):
    """
    CONTRIBUTEUR
    """

    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributors.objects.filter(project_id=self.kwargs["project_pk"])

    def create(self, request, project_pk):
        try:
            data = request.data.copy()
            data.update(project_id=project_pk)
            serializer = ContributorsSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
                serializer.save(project_id=project_pk)
                return Response(
                    {"Message": "Un contributeur a été ajouté au projet."},
                    status=status.HTTP_200_OK,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"Message": "Quelque chose a échoué à cause de {}".format(str(e))},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        contrib = get_object_or_404(Contributors, pk=kwargs["pk"])
        contrib.delete()
        return Response(
            {"Message": "le contributeur a été supprimé projet."},
            status=status.HTTP_200_OK,
        )


class SignUpAPIView(APIView):
    def post(self, request):
        try:
            obj = SignUpSerializer(data=request.data)
            if obj.is_valid():
                obj.save()
                return Response(
                    {"Message": "Votre compte a bien été créé."},
                    status=status.HTTP_200_OK,
                )

            return Response(obj.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"Message": "Quelque chose a échoué à cause de {}".format(str(e))},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProjectsViewset(ModelViewSet):
    """
    PROJET
    """

    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated & Access_Project]

    def get_queryset(self):
        return Projects.objects.filter(author_user_id=self.request.user)

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                serializer.author_user_id = self.request.user
                serializer.save()
                contrib = Contributors.objects.create(
                    user_id=self.request.user.id,
                    project_id=serializer.instance.id,
                    permission=Contributors.P_ALL,
                    role="creator",
                )
                return Response(
                    {"Message": "Le projet a bien été créé."},
                    status=status.HTTP_201_CREATED,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"Message": "Quelque chose a échoué à cause de {}".format(str(e))},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        proj = self.get_object()
        proj.delete()
        return Response(
            {"Message": "Le projet a été supprimé."}, status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        proj = self.get_object()
        proj_serializer = ProjectsSerializer(proj, data=request.data, partial=True)

        if proj_serializer.is_valid():
            proj_serializer.save()
            return Response(
                {"Message": "Le projet a bien été modifié"}, status=status.HTTP_200_OK
            )

        return Response(proj_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
