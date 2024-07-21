from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm, ParetoForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import matplotlib.pyplot as plt
import base64
from io import BytesIO

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

def homepage(request):
    return render(request, 'index.html')

def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    context = {'registerform': form}
    return render(request, 'signup.html', context=context)

def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
    context = {'loginform': form}
    return render(request, 'login.html', context=context)

@login_required
def pareto_chart_view(request):
    if request.method == 'POST':
        form = ParetoForm(request.POST)
        if form.is_valid():
            complaint_types = [ct.strip() for ct in form.cleaned_data['complaint_type'].split(',')]
            number_of_complaints = list(map(int, form.cleaned_data['number_of_complaints'].split(',')))

            # Sort data by 'Number of Complaints'
            sorted_data = sorted(zip(complaint_types, number_of_complaints), key=lambda x: x[1], reverse=True)
            sorted_complaint_types = [x[0] for x in sorted_data]
            sorted_number_of_complaints = [x[1] for x in sorted_data]

            # Calculate percentages
            total_complaints = sum(number_of_complaints)
            percentages = [(nc / total_complaints) * 100 for nc in sorted_number_of_complaints]

            # Create a bar chart
            fig, ax = plt.subplots()
            bars = ax.bar(sorted_complaint_types, percentages)

            # Color bars above 80% differently
            for bar, percentage in zip(bars, percentages):
                if percentage > 80:
                    bar.set_color('red')
                else:
                    bar.set_color('blue')

            ax.set_xlabel('Complaint Type')
            ax.set_ylabel('Percentage')
            ax.set_title('Pareto Chart')

            # Save the plot to a BytesIO object
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # Convert plot to base64 string
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close(fig)

            context = {
                'form': form,
                'chart': image_base64
            }
            return render(request, 'pareto_chart.html', context)
    else:
        form = ParetoForm()

    return render(request, 'pareto_chart.html', {'form': form})

@login_required
def user_logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('index')

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def projects(request):
    return render(request, 'projects.html')

@login_required
def quality_centre(request):
    return render(request, 'quality_centre.html')

@login_required
def analytics(request):
    return render(request, 'analytics.html')