from django.urls import path
from django.contrib.auth import views as auth_view
from . import views
from .views import (expertiseListView, expertiseDetailView,
                    expertiseCreateView, expertiseUpdateView,
                    expertiseDeleteView, UserexpertiseListView,
                    search, filtercategory, CartDeleteView,
                    )

urlpatterns = [
    path('',views.home, name='home'),
    path('user/<str:username>',UserexpertiseListView.as_view(), name='user-expertise'),
    path('category/',views.filtercategory, name='category-expertise'),
    path('expertise/<int:pk>/',expertiseDetailView.as_view(), name='expertise-detail'),
    path('expertise/<int:pk>/update/',expertiseUpdateView.as_view(), name='expertise-update'),
    path('expertise/<int:pk>/delete/',expertiseDeleteView.as_view(), name='expertise-delete'),
    path('expertise/new/',expertiseCreateView.as_view(), name='expertise-create'),
    path('about/',views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('searchresults/', views.search, name='searchresults'),
    path('signup/',  views.signup, name='signup'),
    path('profile/',  views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='ExpertFinder/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='ExpertFinder/logout.html'), name='logout'),
    path('', expertiseListView.as_view(), name='home'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.get_cart_items, name='cart'),
    path('remove-from-cart/<int:pk>/', CartDeleteView.as_view(), name='remove-from-cart'),
    path('ordered/', views.order_item, name='ordered'),
    path('order_details/', views.order_details, name='order_details'),
    path('completed_order/', views.admin_view, name='admin_view'),
    path('pending_orders/', views.pending_orders, name='pending_orders'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update_status/<int:pk>', views.update_status, name='update_status'),
]