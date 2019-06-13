"""ApiSoftwareDesign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from ApiSoftwareDesign import views



urlpatterns = [
				path('admin/', admin.site.urls),
				path('mineral_deposits/', views.MineralDeposit.as_view()),
				path('mineral_deposits/<str:id>/', views.MineralDeposit.as_view()),
				path('block_models/', views.BlockModel.as_view()),

				path('block_models/<str:id>/', views.BlockModel.as_view()),
				path('block_models/<str:id>/data_map', views.DataMap.as_view()),
				path('block_models/<str:id>/blocks/', views.Blocks.as_view()),
				path('block_models/<str:id>/blocks/<str:id_block_param>', views.Blocks.as_view()),
]
