# Generated by Django 4.0.3 on 2022-03-23 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Agents',
            },
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.TextField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], null=True)),
                ('marital_status', models.TextField(choices=[('SINGLE', 'Single'), ('MARRIED', 'Married'), ('DIVORCED', 'Divorced')], null=True)),
                ('source', models.CharField(blank=True, choices=[('Facebook', 'Facebook'), ('Google', 'Google'), ('Youtube', 'Youtube'), ('Medium', 'Medium'), ('Linkedin', 'Linkedin'), ('Blogpost', 'Blogpost'), ('Other', 'Other')], max_length=50, null=True)),
                ('stage', models.CharField(blank=True, choices=[('Prospecting', 'Prospecting'), ('Converted', 'Converted'), ('Lost', 'Lost'), ('New', 'New')], max_length=50, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('is_customer', models.BooleanField(default=False)),
                ('assignee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent', to='crm.agent')),
            ],
            options={
                'verbose_name_plural': 'Leads',
                'ordering': ('-id', '-date_created'),
            },
        ),
    ]
