from django.conf import settings
from django.db import migrations
from django.contrib.auth.models import User


def create_superuser(apps, schema_editor):
    superuser = User.objects.create_superuser(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD
    )
    superuser.save()


class Migration(migrations.Migration):
    dependencies = [
        ('user_interface', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
