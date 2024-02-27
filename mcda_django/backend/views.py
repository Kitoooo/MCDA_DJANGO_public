from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from pymcdm.methods import TOPSIS
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .CSVDataProcessor import CSVDataProcessor


class CSVUploadView(APIView):
    def post(self, request, *args, **kwargs):
        if not self.is_csv(request):
            return Response(
                {"message": "Wrong content type"}, status=status.HTTP_400_BAD_REQUEST
            )

        return self.process_csv(request, **kwargs)

    def is_csv(self, request):
        return request.content_type == "text/csv"

    def process_csv(self, request, **kwargs):
        try:
            processor = self.create_processor(request.body, **kwargs)
            return self.create_success_response(processor)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)  # TODO: logger instead?
            return Response(
                {"message": "Error processing data"}, status=status.HTTP_400_BAD_REQUEST
            )

    def create_processor(self, data, **kwargs):
        method_name = kwargs.get("method_name")
        return CSVDataProcessor(method_name, data)

    def create_success_response(self, processor):
        return Response(
            {
                "message": "CSV data uploaded",
                "preferences": processor.preferences,
                "ranks": processor.ranking,
                "alts_number": processor.alts_number,
            },
            status=status.HTTP_200_OK,
        )
