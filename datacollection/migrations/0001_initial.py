# Generated by Django 3.1.7 on 2021-04-06 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreferenceForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Form Name')),
                ('is_taking_responses', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('course_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_form', to='database.modelset')),
                ('student_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_form', to='database.modelset')),
            ],
        ),
        migrations.CreateModel(
            name='PreferenceFormEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100, verbose_name='Student Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Student Email')),
                ('courses', models.ManyToManyField(to='database.Course')),
                ('preference_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='datacollection.preferenceform')),
            ],
        ),
    ]
