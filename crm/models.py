from django.db import models
from users.models import CustomUser


class Agent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=False, blank=False,
                                related_name='agent')

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = 'Agents'


class Lead(models.Model):
    sources = (('Facebook', 'Facebook'),
               ('Google', 'Google'),
               ('Youtube', 'Youtube'),
               ('Medium', 'Medium'),
               ('Linkedin', 'Linkedin'),
               ('Blogpost', 'Blogpost'),
               ('Other', 'Other'))
    stages = (('Prospecting', 'Prospecting'),
              ('Converted', 'Converted'),
              ('Lost', 'Lost'),
              ('New', 'New'))
    gender_choices = [('MALE', 'Male'), ('FEMALE', 'Female')]
    marital_choices = [('SINGLE', 'Single'), ('MARRIED', 'Married'), ('DIVORCED', 'Divorced')]
    gender = models.TextField(null=True, choices=gender_choices)
    marital_status = models.TextField(null=True, choices=marital_choices)
    source = models.CharField(max_length=50, choices=sources, null=True, blank=True)
    stage = models.CharField(max_length=50, choices=stages, null=True, blank=True, default='New')
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    assignee = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name='agent')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    is_customer = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        ordering = ("-id", "-date_created")
        verbose_name_plural = 'Leads'
        # abstract = True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
