from django.conf import settings
from django.db import migrations
from django.contrib.auth.models import User
from oauth2_provider.models import Application


def create_application(apps, schema_editor):
    superuser = User.objects.get(
        username=settings.ADMIN_USERNAME
    )

    application = Application.objects.create(
        name='user_interface',
        user=superuser,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD
    )
    application.save()


class Migration(migrations.Migration):
    dependencies = [
        ('user_interface', '0002_superuser'),
    ]

    operations = [
        migrations.RunPython(create_application),
    ]
