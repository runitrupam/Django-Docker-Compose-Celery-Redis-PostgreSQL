from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .tasks import my_celery_task

from app.tasks import *
from app.tasks import fibonacci # error as was using the @app.task

import time

class MyApiView(APIView):
    def get(self, request):
        print(request.data,'Get method ') #  {} Get method 

        # Example: Get Fibonacci sequence
        n = int(request.query_params.get('n', 10))  # Default n is 10
        fibonacci_result = fibonacci.delay(n).get()
        
        # Example: Get factorial
        m = int(request.query_params.get('m', 5))  # Default m is 5
        factorial_result = factorial.delay(m).get()
        
        # Example: Get task with delay result
        task_result = task_with_delay.delay().get()
        
        # Example: Get get_name_rr result
        get_name_rr_result = get_name_rr.delay().get()
        
        response_data = {
            'fibonacci_result': fibonacci_result,
            'factorial_result': factorial_result,
            'task_with_delay_result': task_result,
            'get_name_rr_result': get_name_rr_result,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        print(request.data,'Post method')
        # Get request data if needed
        arg1 = request.data.get('arg1')
        arg2 = request.data.get('arg2')

        # Call the Celery task
        result = add.delay(arg1, arg2)
        # Get the task result
        while not result.ready():
            print("Task is still running...")
            time.sleep(1)

        print("Task result:", result.result)
        # You can return a response immediately with a task ID, result.id if needed
        response_data = {'task_id': result.result}

        return Response(response_data, status=status.HTTP_202_ACCEPTED)
