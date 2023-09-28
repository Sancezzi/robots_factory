from django.urls import path

from .views import create_robot_view, RobotExcelExportView

app_name = 'robots'

urlpatterns = [
    path('create_robot/',  create_robot_view, name='create_robot'),
    path('get_excel_data/', RobotExcelExportView.as_view(), name='excel_export/')
]