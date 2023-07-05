# Generated by Django 4.0.4 on 2022-05-14 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('std_id', models.CharField(max_length=5)),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('faculty', models.CharField(choices=[('01', 'Civil'), ('02', 'Computer'), ('03', 'Electrical'), ('04', 'Mechanical')], max_length=10)),
                ('phone', models.CharField(max_length=10)),
                ('Address', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='attendence',
            name='std_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.student'),
        ),
    ]
