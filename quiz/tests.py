import re
import datetime
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from quiz.models import Group, User, Answer, Question
from quiz.views import GroupView, UserView, SelectUserAnswerView, QuestionView, SelectUserCurrentAnswerRateView

factory = APIRequestFactory()
UUID_PATTERN = '[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}'


class TestGroup(TestCase):
    """Groupテスト"""

    def setUp(self):
        """初期処理"""
        Group.objects.create(group_name='名前1', is_deleted=False)
        Group.objects.create(group_name='名前2', is_deleted=False)
        Group.objects.create(group_name='名前3', is_deleted=True)

    def test_get_group_success(self):
        """GETの正常系"""
        request = factory.get('/groups')
        get_groups = GroupView.as_view()
        response = get_groups(request)
        data = response.data.values()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        record1 = data.get(group_name='名前1')

        self.assertTrue(re.match(UUID_PATTERN, str(record1['group_id'])))
        self.assertEqual('名前1', record1['group_name'])
        self.assertEqual(False, record1['is_deleted'])
        self.assertEqual(type(datetime.datetime.today()), type(record1['create_date']))
        self.assertEqual(type(datetime.datetime.today()), type(record1['update_date']))

    def test_post_group_success(self):
        """POST正常系"""

        body = {
            'group_name': 'なぞなぞ'
        }
        request = factory.post('/groups', data=body, format='json')
        post_groups = GroupView.as_view()
        response = post_groups(request)

        obj = Group.objects.get(group_name='なぞなぞ')
        self.assertEqual(response.status_code, 204)
        self.assertTrue(re.match(UUID_PATTERN, str(obj.group_id)))
        self.assertEqual('なぞなぞ', obj.group_name)
        self.assertEqual(False, obj.is_deleted)
        self.assertEqual(type(datetime.datetime.today()), type(obj.create_date))
        self.assertEqual(type(datetime.datetime.today()), type(obj.update_date))


class TestUser(TestCase):
    """Userテスト"""

    def setUp(self):
        """初期処理"""
        User.objects.create(user_name='ユーザ1', mail_address='aiu1@mail.com', is_deleted=False)
        User.objects.create(user_name='ユーザ2', mail_address='aiu2@mail.com', is_deleted=True)
        User.objects.create(user_name='ユーザ3', mail_address='aiu3@mail.com', is_deleted=False)

    def test_get_user_success(self):
        """GETの正常系"""
        request = factory.get('/users')
        get_users = UserView.as_view()
        response = get_users(request)
        data = response.data.values()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        record1 = data.get(user_name='ユーザ1')
        self.assertTrue(re.match(UUID_PATTERN, str(record1['user_id'])))
        self.assertEqual('ユーザ1', record1['user_name'])
        self.assertEqual(False, record1['authority'])
        self.assertEqual(None, record1['correct_answer_rate'])
        self.assertEqual(False, record1['is_deleted'])
        self.assertEqual(type(datetime.datetime.today()), type(record1['create_date']))
        self.assertEqual(type(datetime.datetime.today()), type(record1['update_date']))

    def test_post_user_success(self):
        """POST正常系"""
        body = {
            'user_name': 'ユーザ4',
            'mail_address': 'aiu4@mail.com'
        }

        request = factory.post('/users', data=body, format='json')
        post_user = UserView.as_view()
        response = post_user(request)

        obj = User.objects.get(user_name='ユーザ4')
        self.assertEqual(response.status_code, 204)
        self.assertTrue(re.match(UUID_PATTERN, str(obj.user_id)))
        self.assertEqual('ユーザ4', obj.user_name)
        self.assertEqual('aiu4@mail.com', obj.mail_address)
        self.assertEqual(False, obj.authority)
        self.assertEqual(None, obj.correct_answer_rate)
        self.assertEqual(False, obj.is_deleted)
        self.assertEqual(type(datetime.datetime.today()), type(obj.create_date))
        self.assertEqual(type(datetime.datetime.today()), type(obj.update_date))


class TestSelectUser(TestCase):
    """SelectUserテスト"""

    def setUp(self):
        """初期処理"""
        User.objects.create(user_name='ユーザ1', mail_address='aiu1@mail.com', is_deleted=False)
        User.objects.create(user_name='ユーザ2', mail_address='aiu2@mail.com', is_deleted=True)
        User.objects.create(user_name='ユーザ3', mail_address='aiu3@mail.com', is_deleted=False)

    def test_get_user_success(self):
        """GETの正常系"""

        obj = User.objects.get(user_name='ユーザ3')

        request = factory.get('/users/{}'.format(obj.user_id))
        get_users = UserView.as_view()
        response = get_users(request)
        data = response.data.values()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        record = data.get(user_name='ユーザ3')
        self.assertTrue(re.match(UUID_PATTERN, str(record['user_id'])))
        self.assertEqual('ユーザ3', record['user_name'])
        self.assertEqual('aiu3@mail.com', record['mail_address'])
        self.assertEqual(False, record['authority'])
        self.assertEqual(None, record['correct_answer_rate'])
        self.assertEqual(False, record['is_deleted'])
        self.assertEqual(type(datetime.datetime.today()), type(record['create_date']))
        self.assertEqual(type(datetime.datetime.today()), type(record['update_date']))


class TestSelectUserCurrentAnswerRate(TestCase):
    """SelectUserCurrentAnswerRateテスト"""

    def setUp(self):
        """初期処理"""
        User.objects.create(user_name='ユーザ1', mail_address='aiu1@mail.com', is_deleted=False)
        User.objects.create(user_name='ユーザ2', mail_address='aiu2@mail.com', is_deleted=True)
        User.objects.create(user_name='ユーザ3', mail_address='aiu3@mail.com', is_deleted=False)

        Group.objects.create(group_name='名前1', is_deleted=False)
        Group.objects.create(group_name='名前2', is_deleted=False)
        Group.objects.create(group_name='名前3', is_deleted=True)

        user = User.objects.get(user_name='ユーザ1')
        group = Group.objects.get(group_name='名前2')
        Question.objects.create(
            group_id=group.group_id,
            user_id=user.user_id,
            question_type='select',
            question='問題1',
            correct=1,
            choice_1='a',
            choice_2='b',
            choice_3='c',
            choice_4='d'
        )

        question = Question.objects.get(question='問題1')
        Answer.objects.create(
            user_id=user.user_id,
            question_id=question.question_id,
            group_id=group.group_id,
            answer=1,
            is_correct=True,
            challenge_count=1,
            is_deleted=False
        )
        Answer.objects.create(
            user_id=user.user_id,
            question_id=question.question_id,
            group_id=group.group_id,
            answer=1,
            is_correct=True,
            challenge_count=1,
            is_deleted=False
        )
        Answer.objects.create(
            user_id=user.user_id,
            question_id=question.question_id,
            group_id=group.group_id,
            answer=1,
            is_correct=False,
            challenge_count=2,
            is_deleted=False
        )
        Answer.objects.create(
            user_id=user.user_id,
            question_id=question.question_id,
            group_id=group.group_id,
            answer=1,
            is_correct=True,
            challenge_count=2,
            is_deleted=False
        )
        Answer.objects.create(
            user_id=user.user_id,
            question_id=question.question_id,
            group_id=group.group_id,
            answer=1,
            is_correct=True,
            challenge_count=1,
            is_deleted=True
        )

    def test_get_user_success(self):
        """GETの正常系"""
        user = User.objects.get(user_name='ユーザ1')
        group = Group.objects.get(group_name='名前2')

        request = factory.get('/users/{}/current_answers_rate'.format(user.user_id),
                              data=dict(group_id=group.group_id))

        get_answers = SelectUserCurrentAnswerRateView.as_view()
        response = get_answers(request, user.user_id)
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('correct_answer_rate'), 0.75)
        detail = data.get('detail')
        self.assertEqual(len(detail), 2)
        self.assertEqual(1, detail[0].get('challenge_count'))
        self.assertEqual(1, detail[0].get('correct_answer_rate'))
        self.assertEqual(group.group_id, detail[0].get('group_id'))
        self.assertEqual(2, detail[1].get('challenge_count'))
        self.assertEqual(0.5, detail[1].get('correct_answer_rate'))
        self.assertEqual(group.group_id, detail[1].get('group_id'))


class TestSelectUserAnswer(TestCase):
    """SelectUserAnswerテスト"""

    def setUp(self):
        """初期処理"""
        User.objects.create(user_name='ユーザ1', mail_address='aiu1@mail.com', is_deleted=False)
        User.objects.create(user_name='ユーザ2', mail_address='aiu2@mail.com', is_deleted=True)
        User.objects.create(user_name='ユーザ3', mail_address='aiu3@mail.com', is_deleted=False)

        Group.objects.create(group_name='名前1', is_deleted=False)
        Group.objects.create(group_name='名前2', is_deleted=False)
        Group.objects.create(group_name='名前3', is_deleted=True)

        user = User.objects.get(user_name='ユーザ1')
        group = Group.objects.get(group_name='名前2')
        Question.objects.create(
            group_id=group.group_id,
            user_id=user.user_id,
            question_type='select',
            question='問題1',
            correct=1,
            choice_1='a',
            choice_2='b',
            choice_3='c',
            choice_4='d'
        )

    def test_post_user_success(self):
        """POST正常系"""
        user = User.objects.get(user_name='ユーザ1')
        group = Group.objects.get(group_name='名前3')
        question = Question.objects.get()
        body = dict(
            question_id=question.question_id,
            group_id=group.group_id,
            answer='1',
            is_correct=True,
            challenge_count=1
        )

        request = factory.post('/users/{}/answers'.format(user.user_id), data=body, format='json')
        post_user = SelectUserAnswerView.as_view()
        response = post_user(request, user.user_id)
        self.assertEqual(204, response.status_code)
        record = Answer.objects.get(answer='1', group_id=group.group_id)
        self.assertTrue(re.match(UUID_PATTERN, str(record.answer_id)))
        self.assertEqual(user.user_id, record.user_id)
        self.assertEqual(group.group_id, record.group_id)
        self.assertEqual(question.question_id, record.question_id)
        self.assertEqual('1', record.answer)
        self.assertEqual(1, record.challenge_count)
        self.assertEqual(False, record.is_deleted)
        self.assertEqual(type(datetime.datetime.today()), type(record.create_date))
        self.assertEqual(type(datetime.datetime.today()), type(record.update_date))


class TestQuestion(TestCase):
    """Questionテスト"""

    def setUp(self):
        """初期処理"""
        User.objects.create(user_name='ユーザ1', mail_address='aiu1@mail.com', is_deleted=False)
        User.objects.create(user_name='ユーザ2', mail_address='aiu2@mail.com', is_deleted=True)
        User.objects.create(user_name='ユーザ3', mail_address='aiu3@mail.com', is_deleted=False)

        Group.objects.create(group_name='名前1', is_deleted=False)
        Group.objects.create(group_name='名前2', is_deleted=False)
        Group.objects.create(group_name='名前3', is_deleted=True)

        user = User.objects.get(user_name='ユーザ1')
        group1 = Group.objects.get(group_name='名前1')
        group2 = Group.objects.get(group_name='名前2')
        Question.objects.create(
            group_id=group1.group_id,
            user_id=user.user_id,
            question_type='select',
            question='問題1',
            correct=1,
            choice_1='a',
            choice_2='b',
            choice_3='c',
            choice_4='d'
        )
        Question.objects.create(
            group_id=group1.group_id,
            user_id=user.user_id,
            question_type='select',
            question='問題2',
            correct=1,
            choice_1='a',
            choice_2='b',
            choice_3='c',
            choice_4='d'
        )
        Question.objects.create(
            group_id=group1.group_id,
            user_id=user.user_id,
            question_type='select',
            question='問題3',
            correct=1,
            choice_1='a',
            choice_2='b',
            choice_3='c',
            choice_4='d'
        )
        Question.objects.create(
            group_id=group1.group_id,
            user_id=user.user_id,
            question_type='select',
            question='問題4',
            correct=1,
            choice_1='a',
            choice_2='b',
            choice_3='c',
            choice_4='d'
        )
        Question.objects.create(
            group_id=group1.group_id,
            user_id=user.user_id,
            question_type='select',
            question='問題5',
            correct=1,
            choice_1='a',
            choice_2='b',
            choice_3='c',
            choice_4='d',
            is_deleted=True
        )
        Question.objects.create(
            group_id=group2.group_id,
            user_id=user.user_id,
            question_type='select',
            question='問題6',
            correct=1,
            choice_1='a',
            choice_2='b',
            choice_3='c',
            choice_4='d'
        )

    def test_get_question_success(self):
        """GETの正常系"""
        group = Group.objects.get(group_name='名前1')
        request = factory.get('/questions', data=dict(group_id=group.group_id, limit=3))
        get_questions = QuestionView.as_view()
        response = get_questions(request)
        data = response.data

        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(data))
        self.assertTrue(data[0].get('question_id'))
        self.assertTrue(data[0].get('group_id'))
        self.assertTrue(data[0].get('user_id'))
        self.assertTrue(data[0].get('question_type'))
        self.assertTrue(data[0].get('question'))
        self.assertIsNone(data[0].get('shape_path'))
        self.assertTrue(data[0].get('correct'))
        self.assertTrue(data[0].get('choice_1'))
        self.assertTrue(data[0].get('choice_2'))
        self.assertTrue(data[0].get('choice_3'))
        self.assertTrue(data[0].get('choice_4'))

        # ランダム取得できていることの確認
        response2 = get_questions(request)
        data2 = response2.data
        val1 = val2 = ''
        for d in data:
            q = str(d.get('question_id'))
            val1 += q
        for d in data2:
            q = str(d.get('question_id'))
            val2 += q
        self.assertNotEqual(val1, val2)

    def test_post_question_success(self):
        """POST正常系"""
        user = User.objects.get(user_name='ユーザ1', mail_address='aiu1@mail.com', is_deleted=False)
        group = Group.objects.get(group_name='名前1', is_deleted=False)

        body = dict(
            group_id=group.group_id,
            user_id=user.user_id,
            question_type='select',
            question='問題10',
            correct=1,
            choice_1='a',
            choice_2='b',
            choice_3='c',
            choice_4='d'
        )

        request = factory.post('/questions', data=body, format='json')
        post_question = QuestionView.as_view()
        response = post_question(request)
        self.assertEqual(response.status_code, 204)

        obj = Question.objects.get(question='問題10')
        self.assertTrue(re.match(UUID_PATTERN, str(obj.group_id)))
        self.assertTrue(re.match(UUID_PATTERN, str(obj.user_id)))
        self.assertEqual('select', obj.question_type)
        self.assertEqual('1', obj.correct)
        self.assertEqual('a', obj.choice_1)
        self.assertEqual('b', obj.choice_2)
        self.assertEqual('c', obj.choice_3)
        self.assertEqual('d', obj.choice_4)
        self.assertEqual(False, obj.is_deleted)
        self.assertEqual(type(datetime.datetime.today()), type(obj.create_date))
        self.assertEqual(type(datetime.datetime.today()), type(obj.update_date))