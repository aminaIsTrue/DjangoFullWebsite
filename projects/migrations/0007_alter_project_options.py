# Generated by Django 3.2.5 on 2021-09-14 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20210913_1240'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-vote_total', 'title']},
        ),
    ]
