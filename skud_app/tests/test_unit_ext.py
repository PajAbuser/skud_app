import unittest
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from skud_app.views import SKUDViewSet, OperationViewSet

class TestSKUDViewSet(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SKUDViewSet.as_view()

    def test_export(self):
        request = self.factory.get('/export/', {'id': '12345678-1234-1234-1234-123456789012'})
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_export_logs(self):
        request = self.factory.get('/export_logs/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_export_logs_infile(self):
        operation_id = UUID('12345678-1234-1234-1234-123456789012')
        request = self.factory.get('/export_logs_infile/', {'operation_id': operation_id})
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_add_pass(self):
        data = {'Door': {'UUID': '12345678-1234-1234-1234-123456789012'}}
        request = self.factory.post('/add_pass/', data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_repr_pass(self):
        request = self.factory.get('/passes/1/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_repr_passes(self):
        request = self.factory.get('/passes/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_add_door(self):
        data = {'Door': {'UUID': '12345678-1234-1234-1234-123456789012'}}
        request = self.factory.post('/add_door/', data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_repr_door(self):
        request = self.factory.get('/doors/1/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_repr_doors(self):
        request = self.factory.get('/doors/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_add_door_pass(self):
        data = {'Door': {'UUID': '12345678-1234-1234-1234-123456789012'}, 'Pass': {'UUID': '23456789-2345-2345-2345-234567890123'}}
        request = self.factory.post('/doors/1/passes/', data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_remove_passes(self):
        data = {'Door': {'UUID': '12345678-1234-1234-1234-123456789012'}, 'Passes': [{'UUID': '23456789-2345-2345-2345-234567890123'}]}
        request = self.factory.delete('/doors/1/passes/', data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 204)

    def test_remove_pass(self):
        door_id = 1
        pass_id = 1
        request = self.factory.delete(f'/doors/{door_id}/passes/{pass_id}/')
        response = self.view(request)
        self.assertEqual(response.status_code, 204)

    def test_check1(self):
        data = {'Door': {'UUID': '12345678-1234-1234-1234-123456789012'}, 'Pass': {'UUID': '23456789-2345-2345-2345-234567890123'}}
        request = self.factory.post('/check/', data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_check2(self):
        door_id = 1
        pass_id = 1
        request = self.factory.get(f'/check/{door_id}/{pass_id}/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)


class TestOperationViewSet(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = OperationViewSet.as_view()

    def test_get_operation(self):
        id = UUID('12345678-1234-1234-1234-123456789012')
        request = self.factory.get(f'/getOperation/{id}/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()