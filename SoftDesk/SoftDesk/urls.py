from django.contrib import admin
from django.urls import path, include

# from rest_framework import routers
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ManageAPI.views import (
    SignUpAPIView,
    ContributorsViewset,
    ProjectsViewset,
    IssuesViewset,
    CommentsViewset,
)

# routeur
router = routers.DefaultRouter()
router.register(r"projects", ProjectsViewset, basename="projects")
## generates:
# /projects/
# /projects/{pk}/


user_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
user_router.register(r"users", ContributorsViewset, basename="users")
## generates:
# /projects/{project_pk}/users/
# /projects/{project_pk}/users/{user_pk}/

issues_routeur = routers.NestedSimpleRouter(router, r"projects", lookup="project")
issues_routeur.register(r"issues", IssuesViewset, basename="issues")
## generates:
# /projects/{project_pk}/issues/
# /projects/{project_pk}/issues/{issue_pk}/


comments_routeur = routers.NestedSimpleRouter(issues_routeur, r"issues", lookup="issue")
comments_routeur.register(r"comments", CommentsViewset, basename="comments")
## generates:
# /projects/{project_pk}/issues/{issue_pk}/comments/
# /projects/{project_pk}/issues/{issue_pk}/comments/{pk}/

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    path("api/", include(user_router.urls)),
    path("api/", include(issues_routeur.urls)),
    path("api/", include(comments_routeur.urls)),
    path("api/signup", SignUpAPIView.as_view(), name="signup"),
]
