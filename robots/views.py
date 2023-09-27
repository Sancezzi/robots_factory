import json
from datetime import timedelta
from http import HTTPStatus

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .excel_export import ExcelExporter
from .forms import RobotCreationForm
from .models import Robot


@csrf_exempt
def create_robot_view(request):

    # Обработчик для создания записи о роботе через HTTP POST-запрос.
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = RobotCreationForm(data)

            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Entry created successfully'}, status=HTTPStatus.CREATED)
            else:
                errors = form.errors.get_json_data()
                return JsonResponse({'error': errors}, status=HTTPStatus.BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=HTTPStatus.BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=HTTPStatus.BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=HTTPStatus.METHOD_NOT_ALLOWED)


class RobotExcelExportView(ExcelExporter, View):
    _TIMEINTERVAL= 7 # Получение данных за последние 7 дней

    def get(self, request):
        # Определение даты начала и конца интервала
        end_date = timezone.now()
        start_date = end_date - timedelta(days=self._TIMEINTERVAL)

        robots_data = Robot.objects.filter(created__range=(start_date, end_date))\
            .values_list('model', 'version')\
            .annotate(count=Count('serial'))\
            .order_by('serial')
        
        # Создание Excel-файла на основе данных или пустого файла, если данных нет
        if robots_data:
            excel_data = self.create_data_excel(robots_data)
        else:
            excel_data = self.create_blank_excel()

        # Создание HTTP-ответа с содержимым Excel-файла для скачивания
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=report_on_produced_robots.xlsx'
        response.write(excel_data)
        return response


