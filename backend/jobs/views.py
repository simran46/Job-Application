import json
from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Job
from .serializers import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def _parse_multiselect_data(self, request_data):
        """
        Helper to convert potential string-encoded JSON or multi-valued form fields
        for 'status' and 'category' into Python list format before serialization.
        Handles both dict-like structures (JSON requests) and QueryDict (form-data).
        """
        data = {}
        is_querydict = hasattr(request_data, 'getlist')
        
        # Get all keys in request data
        for key in request_data.keys():
            if key in ['status', 'category']:
                if is_querydict:
                    list_val = request_data.getlist(key)
                else:
                    val = request_data.get(key)
                    if isinstance(val, list):
                        list_val = val
                    else:
                        list_val = [val] if val is not None else []
                
                # Parse internal items
                parsed_list = []
                for item in list_val:
                    if isinstance(item, str):
                        item_stripped = item.strip()
                        if item_stripped.startswith('[') and item_stripped.endswith(']'):
                            try:
                                parsed_list.extend(json.loads(item_stripped))
                            except json.JSONDecodeError:
                                parsed_list.extend([v.strip() for v in item_stripped[1:-1].split(',') if v.strip()])
                        elif ',' in item_stripped:
                            parsed_list.extend([v.strip() for v in item_stripped.split(',') if v.strip()])
                        elif item_stripped:
                            parsed_list.append(item_stripped)
                    else:
                        parsed_list.append(item)
                data[key] = parsed_list
            else:
                data[key] = request_data.get(key)
        return data

    def create(self, request, *args, **kwargs):
        # Parse data to ensure multiselect fields are clean list structures
        parsed_data = self._parse_multiselect_data(request.data)
        
        serializer = self.get_serializer(data=parsed_data)
        serializer.is_valid(raise_exception=True)
        
        # Assign order as max(order) + 1 to place new jobs at the end
        max_order = Job.objects.aggregate(models.Max('order'))['order__max']
        order = (max_order + 1) if max_order is not None else 0
        
        serializer.save(order=order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        parsed_data = self._parse_multiselect_data(request.data)
        
        serializer = self.get_serializer(instance, data=parsed_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """
        Clones a job and inserts it exactly below the parent job.
        """
        source_job = self.get_object()
        
        # Clone fields
        new_job = Job(
            title=f"{source_job.title} (Copy)",
            status=source_job.status,
            category=source_job.category,
            address=source_job.address,
            city=source_job.city,
            state=source_job.state,
            start_date=source_job.start_date,
            end_date=source_job.end_date,
            description=source_job.description,
            profile_picture=source_job.profile_picture,
            order=source_job.order + 1
        )
        
        # Increment all orders after the source job's order
        Job.objects.filter(order__gt=source_job.order).update(order=models.F('order') + 1)
        new_job.save()
        
        serializer = self.get_serializer(new_job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
