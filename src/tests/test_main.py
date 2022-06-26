import json
from unittest import mock, TestCase

from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


class PingViewTest(TestCase):
    def test_pong_200(self):
        response = client.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'pong')


class MustBeAuthenticatedMixin:
    endpoint = ''
    headers = {'Authorization': 'Bearer test-key'}

    def test_not_authenticated_403(self):
        response = client.post(self.endpoint)
        self.assertEqual(response.status_code, 403)


class TrainPipelinesViewTest(MustBeAuthenticatedMixin, TestCase):
    endpoint = '/train_pipelines'

    def test_task_called_200(self):
        with mock.patch(
            'src.main.task_train_and_select_pipelines.delay'
        ) as mock_task_delay:
            response = client.post(self.endpoint, headers=self.headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), 'Training pipelines')
            self.assertEqual(mock_task_delay.call_count, 1)


class PredictAttendingViewTest(MustBeAuthenticatedMixin, TestCase):
    endpoint = '/predict_attending'

    def setUp(self) -> None:
        self.post_data = {
            'gender': 1,
            'scheduled_day': '1994-08-08T00:00:00Z',
            'appointment_day': '1994-07-28T00:00:00Z',
            'age': 28,
            'neighbourhood': 'Vallecas',
            'scholarship': 0,
            'hypertension': 0,
            'diabetes': 0,
            'alcoholism': 0,
            'handicap': 0,
            'sms_received': 1,
        }

    def test_predict_200(self):
        with mock.patch(
            'src.main.SenniorsPredictor'
        ) as mock_senniors_predictor:
            predict_value = True
            mock_predictor = mock.MagicMock()
            mock_predictor.predict.return_value = predict_value
            mock_senniors_predictor.return_value = mock_predictor
            response = client.post(
                self.endpoint,
                headers=self.headers,
                data=json.dumps(self.post_data),
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {
                    'attending': predict_value
                }
            )
            self.assertEqual(mock_senniors_predictor.call_count, 1)

    def test_predict_but_not_valid_pipeline_404(self):
        with mock.patch(
            'src.main.SenniorsPredictor'
        ) as mock_senniors_predictor:
            mock_senniors_predictor.side_effect = ValueError()
            response = client.post(
                self.endpoint,
                headers=self.headers,
                data=json.dumps(self.post_data),
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                response.json(),
                {
                    'detail': (
                        'There is not a valid pipeline, please wait until it is trained or call the train_pipelines '
                        'endpoint'
                    )
                }
            )
