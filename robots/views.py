import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import RobotCreationForm


@csrf_exempt
def create_robot_view(request):
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

