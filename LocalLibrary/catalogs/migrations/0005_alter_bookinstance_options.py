# Generated by Django 4.0 on 2022-12-07 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0004_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_as_returned', 'set_book_as_returned'),)},
        ),
    ]