import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question

# Create your tests here.

def create_question(question_text, days):
    """
    Create (return) the Question object with certainly text and published
    given numbers of days offset now (positive to the future and negative to the past)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() retuns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist an appropriate message are displayed
        """
        response = self.client.get(reverse("pools:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available.")
        self.assertQuerySetEqual(response.context["latest_qs"], [])

    def test_past_question(self):
        """
        If the question with pub_date in the past it is displayed
        :return:
        """
        q = create_question(question_text="Past question.", days=-20)
        response = self.client.get(reverse("pools:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_qs"], [q])

    def test_future_question(self):
        """Future question is not published"""
        q = create_question(question_text="Future question", days=20)
        response = self.client.get(reverse("pools:index"))
        self.assertContains(response, "No polls available.")
        self.assertQuerySetEqual(response.context["latest_qs"], [])

class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        """Details of past question are published"""
        q = create_question(question_text="Past question.", days=-1)
        response = self.client.get(reverse("pools:details", args=[q.id,]))
        self.assertContains(response, q.question_text)

    def test_future_question(self):
        """Details of future question aren't published"""
        q = create_question(question_text="Future question.", days=2)
        response = self.client.get(reverse("pools:details", args=[q.id,]))
        self.assertEqual(response.status_code, 404)

class QuestionResultsViewTests(TestCase):
    def test_past_question(self):
        """Results of past question are published"""
        q = create_question(question_text="Past question.", days=-1)
        response = self.client.get(reverse("pools:results", args=[q.id,]))
        self.assertContains(response, q.question_text)

    def test_future_question(self):
        """Results of Future question is not published"""
        q = create_question(question_text="Future question", days=20)
        response = self.client.get(reverse("pools:results", args=[q.id,]))
        self.assertEqual(response.status_code, 404)
