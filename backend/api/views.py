from django.http import JsonResponse


def api_home(request):
    return JsonResponse({'msg': 'hi'})
