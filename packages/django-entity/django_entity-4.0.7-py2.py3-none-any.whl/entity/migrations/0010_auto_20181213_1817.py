# Generated by Django 2.1.4 on 2018-12-13 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('entity', '0009_auto_20180402_2145'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='entity',
            unique_together={('entity_id', 'entity_type')},
        ),
    ]
