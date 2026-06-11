from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Job

class JobAPITests(APITestCase):
    def setUp(self):
        # Create a few jobs to test ordering and duplication
        self.job1 = Job.objects.create(
            title="Job 1",
            status=["Draft"],
            category=["Full-time"],
            address="123 St",
            city="City A",
            state="State A",
            order=0
        )
        self.job2 = Job.objects.create(
            title="Job 2",
            status=["Posted"],
            category=["Part-time"],
            address="456 Rd",
            city="City B",
            state="State B",
            order=1
        )
        self.list_url = reverse('job-list')
        self.detail_url = lambda pk: reverse('job-detail', kwargs={'pk': pk})
        self.duplicate_url = lambda pk: reverse('job-duplicate', kwargs={'pk': pk})

    def test_list_jobs(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], "Job 1")
        self.assertEqual(response.data[1]['title'], "Job 2")

    def test_create_job(self):
        data = {
            "title": "Job 3",
            "status": "Draft,Requested",
            "category": '["Full-time", "Intern"]',
            "address": "789 Ave",
            "city": "City C",
            "state": "State C",
            "description": "Needs description"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Job 3")
        self.assertEqual(response.data['status'], ["Draft", "Requested"])
        self.assertEqual(response.data['category'], ["Full-time", "Intern"])
        self.assertEqual(response.data['order'], 2) # check order sequence is auto-incremented

    def test_edit_job(self):
        data = {
            "title": "Job 2 Edited",
            "status": ["Filled"],
            "category": ["Part-time"]
        }
        # Update using PATCH
        response = self.client.patch(self.detail_url(self.job2.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Job 2 Edited")
        self.assertEqual(response.data['status'], ["Filled"])

    def test_delete_job(self):
        response = self.client.delete(self.detail_url(self.job1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Job.objects.filter(pk=self.job1.pk).exists())

    def test_duplicate_job(self):
        # We duplicate Job 1, which has order=0. The duplicate should get order=1.
        # Job 2 (which had order=1) should be bumped to order=2.
        response = self.client.post(self.duplicate_url(self.job1.pk))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        duplicate_id = response.data['id']
        duplicate_job = Job.objects.get(pk=duplicate_id)
        
        # Verify duplicate details
        self.assertEqual(duplicate_job.title, "Job 1 (Copy)")
        self.assertEqual(duplicate_job.order, 1)
        
        # Refresh Job 2 and verify its order was bumped to 2
        self.job2.refresh_from_db()
        self.assertEqual(self.job2.order, 2)
        
        # Check ordering of list endpoint
        response = self.client.get(self.list_url)
        self.assertEqual(response.data[0]['title'], "Job 1")
        self.assertEqual(response.data[1]['title'], "Job 1 (Copy)")
        self.assertEqual(response.data[2]['title'], "Job 2")
