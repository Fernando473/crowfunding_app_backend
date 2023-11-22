from django.db import models


# Create your models here.
class Entrepreneur(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)
    project_description = models.CharField(max_length=1000)
    objective_amount = models.FloatField(default=0)
    current_amount = models.FloatField(default=0)
    image = models.CharField(max_length=500)
    entrepreneur = models.ForeignKey(Entrepreneur, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Investor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    monto = models.FloatField(default=0)

    def __str__(self):
        return self.project.name + self.investor.name
