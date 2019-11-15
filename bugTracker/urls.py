"""bugTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bugTracker import views
# from django.contrib.auth.models import User
from bugTracker.models import Ticket

# admin.site.register(User)
admin.site.register(Ticket)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_user_view, name='register'),
    path('addticket/', views.create_new_ticket, name='addticket'),
    path('user/<int:id>', views.user_detail_view),
    path('assign/<int:id>', views.assign_ticket),
    path('edit/<int:id>', views.ticket_edit),
    path('invalidate/<int:id>', views.mark_ticket_invalid),
    path('complete/<int:id>', views.complete_ticket),
    path('unassign/<int:id>', views.unassign_ticket),
    path('incomplete/<int:id>', views.uncomplete_ticket),
    path('validate/<int:id>', views.make_invalid_ticket_valid),
    path('ticket/<int:id>', views.ticket_detail_view, name='ticket')
]
