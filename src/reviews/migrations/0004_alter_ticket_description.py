# Generated by Django 4.0.2 on 2022-04-12 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_review_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(blank=True, default="L'avez-vous lu ?", max_length=2048),
        ),
    ]
