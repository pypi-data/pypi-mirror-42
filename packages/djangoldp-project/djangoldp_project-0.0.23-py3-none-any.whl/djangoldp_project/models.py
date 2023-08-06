from django.contrib.auth.models import User
from django.db import models

from djangoldp.models import Model


class Customer(Model):
    name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    logo = models.URLField()
    companyRegister = models.CharField(default='', max_length=255)
    firstName = models.CharField(default='', max_length=255)
    lastName = models.CharField(default='', max_length=255)
    role = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(default='')
    phone = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        permissions = (
            ('view_client', 'Read'),
            ('control_client', 'Control'),
        )

    def __str__(self):
        return self.name


class Project(Model):
    name = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    number = models.PositiveIntegerField(default='0', blank=True)
    creationDate = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)  # WARN add import
    team = models.ManyToManyField(User, through='Member', blank=True)
    businessProvider = models.CharField(max_length=255, blank=True, null=True)
    businessProviderFee = models.PositiveIntegerField(default='0', blank=True)
    jabberID = models.CharField(max_length=255, blank=True, null=True)
    jabberRoom = models.BooleanField(default=True)

    @classmethod
    def get_view_set(cls):
        from djangoldp_project.views import ProjectViewSet
        return ProjectViewSet

    class Meta:
        permissions = (
            ('view_project', 'Read'),
            ('control_project', 'Control'),
        )
        rdf_type = 'doap:project'

    def __str__(self):
        return self.name


Project._meta.serializer_fields = ['@id', 'name', 'description', 'creationDate', 'team', 'businessProvider',
                                   'businessProviderFee', 'number', 'members', 'customer', 'jabberID', 'jabberRoom']


class Member(Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


Member._meta.container_path = "project-members/"
