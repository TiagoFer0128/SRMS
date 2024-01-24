from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import CreateRequestSerializer, GoogleTextSearchSerializer, GooglePlaceIdSerializer
from services.common import CommonService
from services.bookingengineservice import BookingEngineService
from services.google_map_service import GoogleMapService

# Create your views here.
class BookingEngineViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = CreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            search = serializer.validated_data.get("search")
            booking_type = serializer.validated_data.get("booking_type")
            result = BookingEngineService().processSearch(search)
            # result = {
            #     "data": {
            #         "search": search,
            #         "booking_type": booking_type
            #     }
            # }
            return Response(result)
        except ValueError as e:
            return Response({"message": "Invalid json request", "status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # return Response({"message": e, "status": "error"}, status=500)
            return Response({"message": "Server Error!", "status": "error"}, status=500)
        
    @action(detail=False, methods=['POST'], url_path='google-text-search')
    def google_text_search(self, request):
        serializer = GoogleTextSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            location = serializer.validated_data.get("location")
            result = GoogleMapService().text_search(location)
            return Response({
                "success": True,
                "data": result
            })
        except Exception as e:
            return Response({"message": "Server Error!", "status": "error"}, status=500)
        

    @action(detail=False, methods=['POST'], url_path='google-place-search')
    def google_place_search(self, request):
        serializer = GoogleTextSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            location = serializer.validated_data.get("location")
            result = GoogleMapService().search_places_with_combined_methods(location)
            return Response({
                "success": True,
                "data": result
            })
        except Exception as e:
            return Response({"message": "Server Error!", "status": "error"}, status=500)
        
    @action(detail=False, methods=['POST'], url_path='google-map-placeid-data')
    def google_lat_lng_from_placeid(self, request):
        serializer = GooglePlaceIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            place_id = serializer.validated_data.get("place_id")
            result = GoogleMapService().lat_lng_from_place_id(place_id)
            return Response({
                "success": True,
                "data": result
            })
        except Exception as e:
            return Response({"message": "Server Error!", "status": "error"}, status=500)