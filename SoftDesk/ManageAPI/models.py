from django.db import models
from django.contrib.auth.models import User


class Projects(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    type = models.CharField(max_length=50)
    author_user_id = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="project_created",
    )

    def __str__(self):
        return self.title


class Contributors(models.Model):
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    P_NO = "NO"
    P_ALL = "ALL"
    CHOICES = (
        (P_NO, "No permissions"),
        (P_ALL, "Actualise/Delete"),
    )
    permission = models.CharField(max_length=50, choices=CHOICES)
    role = models.CharField(max_length=50)

    def __str__(self):
        return "User ID:{} Project ID:{}".format(self.user_id, self.project_id)


class Issues(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    tag = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    status = models.CharField(max_length=50)
    author_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="issue_created",
    )
    assignee_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="issue_assigned",
    )
    created_time = models.DateTimeField()

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment_id = models.IntegerField()
    description = models.CharField(max_length=300)
    status = models.CharField(max_length=50)
    author_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="comment_created",
    )
    issue = models.ForeignKey(
        Issues,
        on_delete=models.CASCADE,
        related_name="comment",
    )
    created_time = models.DateTimeField()

    def __str__(self):
        return self.description
