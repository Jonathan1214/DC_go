from .import models  # 同一级引用还要这么搞呀！真的会烦死人的
# 我估计是这个结构设计的不对 没有按照官方文档来 不过事已至此 不可挽回了
from django.urls import reverse
from django.test import TestCase


'''
assertions: assertTrue()
            assertEqual()
            assertRaiseMessage()
            assertWarnsMessage()
            assertFieldOutput()
            assertFormError()
            assertFormsetError()
            asssertionContains()
            assertNotContains()
            assertTemplateUsed()
            assertTemplateNotUsed()
            assertRedirects()
            assertHTMLEqual()
            assertHTMLNotEqual()
            assertXMLEqual()
            assertXMLNotEqual()

            assertQuerysetEqual()

'''


# Create your tests here.
class HomeTest(TestCase):
    def test_home_view_status_code(self):
        url = reverse('index:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class StudentTest(TestCase):
    def setUp(self):
        models.Student.objects.create(
            student_num='1170500412', student_name='马子豪', pwd='1170500412')

    def test_student_name_euqal_num(self):
        mzh = models.Student.objects.get(student_name='马子豪')
        self.assertEqual(mzh.student_num, '1170500412')
        self.assertEqual(mzh.pwd, '1170500412')


class LoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up data for the whole TestCase
        pass
