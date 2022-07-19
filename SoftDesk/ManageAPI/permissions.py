from rest_framework.permissions import BasePermission
from ManageAPI.models import Contributors


class DeleteModify_Issue_AuthorOnly(BasePermission):
    """
    Autorise la modification/suppression d'une issue uniquement par son créateur
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "PUT" or request.method == "DELETE":
            return request.user == obj.author_user
        else:
            return True


class Access_Project(BasePermission):
    """
    Autorise l'accès au projet uniquement pour son créateur ou ses contributerus
    Autorise la modification/suppression du projet uniquement par son créateur
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author_user_id:
            return True
        else:
            for contrib in Contributors.objects.filter(project_id=obj.id):
                if contrib.user_id == request.user.id:
                    print(contrib.user_id)
                    if request.method == "PUT" or request.method == "DELETE":
                        return contrib.permission == "ALL"
                    else:
                        return True
        return False


class Access_Comment(BasePermission):
    """
    Autorise l'accès au commentaire uniquement pour son créateur ou pour les contributerus au projet
    Autorise la modification/suppression du commentaire uniquement par son créateur
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj.issue.project.author_user_id:  # createur du projet
            return True
        else:
            for contrib in Contributors.objects.filter(project_id=obj.issue.project.id):
                if contrib.user_id == request.user.id:
                    print(contrib.user_id)
                    print("contributeur reconnu")
                    if request.method == "PUT" or request.method == "DELETE":
                        return False
                    else:
                        return True
        return False
