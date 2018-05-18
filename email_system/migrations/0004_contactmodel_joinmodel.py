# Generated by Django 2.0.5 on 2018-05-18 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('email_system', '0003_delete_mailmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('from_email', models.EmailField(max_length=254)),
                ('subject', models.CharField(blank=True, max_length=100, null=True, verbose_name='Subject')),
                ('message', models.CharField(blank=True, max_length=500, null=True, verbose_name='Message')),
            ],
        ),
        migrations.CreateModel(
            name='JoinModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('from_email', models.EmailField(max_length=254)),
                ('major', models.CharField(blank=True, max_length=500, null=True, verbose_name='Major')),
                ('gradDate', models.CharField(blank=True, max_length=500, null=True, verbose_name='Graduation Date')),
                ('courses', models.CharField(blank=True, max_length=500, null=True, verbose_name='Courses Taken')),
                ('languages', models.CharField(blank=True, max_length=500, null=True, verbose_name='Programming Languages')),
                ('tools', models.CharField(blank=True, max_length=500, null=True, verbose_name='Development Tools')),
                ('whyCAM2', models.CharField(blank=True, max_length=500, null=True, verbose_name='Reason to Join')),
                ('anythingElse', models.CharField(blank=True, max_length=500, null=True, verbose_name='Additional Information')),
            ],
        ),
    ]
