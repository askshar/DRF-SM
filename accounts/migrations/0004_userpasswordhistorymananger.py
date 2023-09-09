# Generated by Django 4.2.4 on 2023-08-30 06:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_alter_userconfig_options_userconfig_generation_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPasswordHistoryMananger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('password', models.CharField(blank=True, max_length=155, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recent_password', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Password History Manager',
            },
        ),
    ]
