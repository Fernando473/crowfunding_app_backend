from rest_framework import serializers
from .models import Project, Investor, Entrepreneur, Transaction


class EntrepreneurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entrepreneur
        fields = ['id', 'name', 'email', 'password']


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'project_description', 'objective_amount', 'current_amount', 'image', 'entrepreneur',
                  'entrepreneur_id']


class InvestorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Investor
        fields = ['id', 'name', 'email', 'password']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'investor', 'project', 'monto']
