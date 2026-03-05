from django.urls import path
from . import views

app_name = 'tracker'  # ← Add this line

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('categories/', views.manage_categories, name='manage_categories'),
]