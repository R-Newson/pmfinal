from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, homepage, signup, user_login, user_logout, index, about, projects, quality_centre, analytics, pareto_chart_view

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    path('projects/', projects, name='projects'),
    path('quality_centre/', quality_centre, name='quality_centre'),
    path('api/', include(router.urls)),
    path('analytics/', analytics, name='analytics'),
    path('pareto/', views.pareto_chart_view, name='pareto_chart_view'),
]
