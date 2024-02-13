from django.http import HttpResponseForbidden
from .models import Task

class TaskOwnershipMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'pk' in view_kwargs:
            task_id = view_kwargs['pk']
            try:
                task = Task.objects.get(pk=task_id)
                if request.user != task.owner:
                    return HttpResponseForbidden("You don't have permission to perform this action.")
            except Task.DoesNotExist:
                return HttpResponseForbidden("Task not found.")
        return None
