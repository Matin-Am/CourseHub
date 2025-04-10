# Generated by Django 5.1.7 on 2025-04-10 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_course_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='episode',
            options={'ordering': ('created',)},
        ),
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%M/%d/'),
        ),
    ]
