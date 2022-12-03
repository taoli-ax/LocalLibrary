# Generated by Django 4.0 on 2022-12-03 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, choices=[('EN', 'English'), ('CN', 'Chinese')], default='EN', max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='lan',
            field=models.ManyToManyField(to='catalogs.Language'),
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='lan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogs.language'),
        ),
    ]