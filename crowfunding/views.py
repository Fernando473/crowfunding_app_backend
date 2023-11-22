from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Entrepreneur, Project, Investor, Transaction
from .serializers import EntrepreneurSerializer, ProjectSerializer, InvestorSerializer, TransactionSerializer


# Create your views here.
class EntrepreneurViewSet(viewsets.ModelViewSet):
    queryset = Entrepreneur.objects.all()
    serializer_class = EntrepreneurSerializer

    def list(self, request):
        email = request.query_params.get('email', None)
        if email:
            try:
                entrepreneur = Entrepreneur.objects.filter(email=email).first()

                serializer = self.serializer_class(entrepreneur, context={'request': request})
                return Response(serializer.data)
            except Entrepreneur.DoesNotExist:
                return Response({'message': 'No entrepreneur found'})
        else:
            try:
                entrepreneurs = Entrepreneur.objects.all()
                serializer = self.serializer_class(entrepreneurs, many=True,
                                                   context={'request': request})  # Pasa el contexto de la solicitud
                return Response(serializer.data, status=200)
            except Entrepreneur.DoesNotExist:
                return Response({'message': 'No entrepreneurs found'})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request):
        entrepreneur_id = request.query_params.get('entrepreneur_id', None)
        if entrepreneur_id:
            try:
                projects = Project.objects.filter(entrepreneur_id=entrepreneur_id)
                if not projects:
                    return Response({'message': 'No Projects found for the entrepreneur.'})
                serializer = self.serializer_class(projects, many=True,
                                                   context={'request': request})  # Pasa el contexto de la solicitud
                return Response(serializer.data)
            except Project.DoesNotExist:
                return Response({'message': 'Projects not found for the entrepreneur.'})
        else:
            try:
                projects = Project.objects.all()
                serializer = self.serializer_class(projects, many=True,
                                                   context={'request': request})  # Pasa el contexto de la solicitud
                return Response(serializer.data)
            except Project.DoesNotExist:
                return Response({'message': 'No projects found'})

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        project_description = request.data.get('project_description')
        objective_amount = request.data.get('objective_amount')
        image = request.data.get('image')
        entrepreneur = request.data.get('entrepreneur')

        project = Project(name=name, project_description=project_description,
                          objective_amount=objective_amount, image=image, entrepreneur_id=entrepreneur)
        project.save()
        return Response({'message': 'Project created!'})


class InvestorViewSet(viewsets.ModelViewSet):
    serializer_class = InvestorSerializer
    queryset = Investor.objects.all()

    def list(self, request):
        email = request.query_params.get('email', None)
        investor_id = request.query_params.get('id', None)

        if email:
            try:
                investor = Investor.objects.get(email=email)
                serializer = self.serializer_class(investor,
                                                   context={'request': request})  # Pasa el contexto de la solicitud
                return Response(serializer.data)
            except Investor.DoesNotExist:
                return Response({'message': 'El inversor no fue encontrado.'}, status=404)

        elif investor_id:
            try:
                investor = Investor.objects.get(pk=investor_id)
                serializer = self.serializer_class(investor,
                                                   context={'request': request})  # Pasa el contexto de la solicitud
                return Response(serializer.data)
            except Investor.DoesNotExist:
                return Response({'message': 'El inversor no fue encontrado.'}, status=404)
        else:
            try:
                investors = Investor.objects.all()
                serializer = self.serializer_class(investors, many=True,
                                                   context={'request': request})  # Pasa el contexto de la solicitud
                return Response(serializer.data)
            except Investor.DoesNotExist:
                return Response({'message': 'No investors found'})


class TransactionViesSets(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def list(self, request):
        try:
            transactions = Transaction.objects.all()
            serializer = self.serializer_class(transactions, many=True,
                                               context={'request': request})  # Pasa el contexto de la solicitud
            return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response({'message': 'No transactions found'})


class InvestInProject(APIView):
    def post(self, request, project_id, investor_id):
        try:
            investor = Investor.objects.get(pk=investor_id)
            project = Project.objects.get(pk=project_id)
        except Investor.DoesNotExist:
            return Response({f'message': f'Investor with id {investor_id} does not exist'})
        except Project.DoesNotExist:
            return Response({f'message': f'Investor with id {project_id} does not exist'})

        existing_investor = Transaction.objects.filter(investor=investor, project=project)

        if existing_investor:
            return Response({'message': 'Investor have been on this project'})

        amount = request.data.get('amount')
        if not amount:
            return Response({'message': 'Amount must be set'})
        if amount < 0:
            return Response({'message': 'Amount must not be 0'})

        if project.current_amount + amount > project.objective_amount:
            return Response({'The project have been reach its goal'})

        transaction = Transaction(investor=investor, project=project)
        transaction.save()

        project.current_amount += amount
        project.save()

        return Response({'message': 'Transaction was successful '}, status=200)
