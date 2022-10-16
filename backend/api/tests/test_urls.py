# from http import HTTPStatus

# from django.test import Client, TestCase

# from users.models import CustomUser, Follow

# # from rest_framework.authentication 

# class UsersURLTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.user = CustomUser.objects.create_user(
#             username='test_username',
#             email='test@mail.com',
#             first_name='test_name',
#             last_name='test_surname',
#             password='Zz12345678'
#         )
#         cls.urls = {
#             'GET': [
#                 ['/api/users/', HTTPStatus.OK],
#                 ['/api/users/1/', HTTPStatus.OK],
#         #         ('/users/me/', HTTPStatus.OK),
#             ]
#         #     'POST': [
#         #         ('/users/', HTTPStatus.CREATED),
#         #         ('/users/set_password/', HTTPStatus.NO_CONTENT),
#         #         ('/auth/token/login/', HTTPStatus.CREATED),
#         #         ('/auth/token/logout/', HTTPStatus.CREATED),
#         #     ] 
#         }

#     def setUp(self):
#         self.guest_client = Client()
#         self.authorized_client = Client()
#         self.authorized_client.force_authenticate(self.user)

#     def test_urls_GET_requests(self):
#         urls = self.urls['GET']
#         print(urls)

#         for url, status_code in urls:
#             with self.subTest(address=url):
#                 response = self.authorized_client.get(url)
#                 self.assertEqual(response.status_code, status_code)
