# Generated by Django 3.1.14 on 2025-01-03 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_auto_20250103_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='description',
            field=models.TextField(),
            preserve_default=False,
        ),
    ]
