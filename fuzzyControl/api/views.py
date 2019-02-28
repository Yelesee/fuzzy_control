from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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

        # make instance of run in setup.py.

        content = {'xmlid': xml_id, 'inputAmount': input_amount,'token':token}
        return Response(content)
