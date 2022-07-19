# Generated by Django 4.0 on 2022-01-13 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('ManageAPI', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='project_id',
        ),
        migrations.AlterField(
            model_name='comments',
            name='author_user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_created', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='issues',
            name='assignee_user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='issue_assigned', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='issues',
            name='author_user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='issue_created', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='author_user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_created', to='auth.user'),
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
