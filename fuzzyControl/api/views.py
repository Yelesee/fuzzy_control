from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import sys
from fuzzy import setup
import ast

sys.path.append("..")


class FuzzyView(APIView):
    permission_classes = (IsAuthenticated,)

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    # return super(FuzzyView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):
        xml_id = request.POST['xml_id']
        input_amount = request.POST.get('input_amount')
        token = request.META['HTTP_AUTHORIZATION']

        input_amount_list = ast.literal_eval(input_amount)
        se = setup.Run(input_amount_list)
        se.final
        # make instance of run in setup.py.

        content = {'xmlid': xml_id, 'inputAmount': input_amount, 'token': token, 'input_amount_list': input_amount_list, 'se.final': se.final}
        return Response(content)
