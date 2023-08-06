import datetime
import json

import requests
from random import randint

import sys


class Api:
    def __init__(self, api_url, api_key, task_id, debug=False):
        self._api_url = api_url
        self._api_key = api_key
        self._task_id = task_id
        self._debug = debug
        self._session = None

    def connect(self):
        session = requests.Session()
        header = {'Authorization': 'ApiKey {}'.format(self._api_key)}
        session.headers.update(header)
        self._session = session

    def disconnect(self):
        self._session.__exit__()
        self._session = None

    def existing_instances(self):
        return self._get_paged('/api/tasks/{}/instances?perPage=1000'.format(self._task_id))

    def create_instance(self, instance):
        return self._post('/api/tasks/{}/instances'.format(self._task_id), instance.as_dict())

    def get_task(self):
        return self._get('/api/tasks/{}'.format(self._task_id))

    def submit_task(self):
        return self._post('/api/tasks/{}/submit'.format(self._task_id))

    def submit_feedback(self, instance_id, iteration_id, expected, provided):
        return self._post('/api/tasks/{}/instances/{}/iterations/{}/feedback'
                          .format(self._task_id, instance_id, iteration_id), [{'segment': None,
                                                                               'provided': json.dumps(provided),
                                                                               'expected': json.dumps(expected)}])

    def submit_feedbacks(self, instance_id, iteration_id, feedbacks):
        return self._post('/api/tasks/{}/instances/{}/iterations/{}/feedback'
                          .format(self._task_id, instance_id, iteration_id), list(map(lambda f: {'segment': f['segment'],
                                                                                            'provided': json.dumps(
                                                                                                f['provided']),
                                                                                            'expected': json.dumps(
                                                                                                f['expected'])},
                                                                                 feedbacks))
                          )

    def get_results(self):
        five_minutes_ago = (datetime.datetime.utcnow() -
                            datetime.timedelta(minutes=5)).isoformat()
        url = '/api/tasks/{0}/results?incIncompleteInstances=true&incIterations=true&asOfUtc={1}&perPage=1000'.format(
            self._task_id,
            five_minutes_ago
        )
        return self._get_paged(url)

    def reiterate(self, instance_id):
        return self._post('/api/tasks/{0}/instances/{1}/reiterate'.format(self._task_id, instance_id))

    def get_qualifications(self):
        return self._get('/api/qualifications')

    def add_qualification(self, instance_id, qual_id):
        return self._post('/api/tasks/{0}/instances/{1}/qualifications/{2}'.format(self._task_id, instance_id, qual_id))

    def _get(self, path):
        response = self._session.get(self._api_url + path)
        response.raise_for_status()
        return response.json()

    def _get_paged(self, path):
        next_path = path
        result = []
        while next_path is not None:
            response = self._session.get(self._api_url + next_path)
            response.raise_for_status()
            result += response.json()
            n = response.links["next"] if "next" in response.links else None
            if n is not None:
                next_path = n["url"]
            else:
                next_path = None

        return result

    def _post(self, path, payload=None):
        if not self._debug:
            response = self._session.post(self._api_url + path, json=payload)
            response.raise_for_status()

            try:
                return response.json()
            except ValueError:
                # Response contained no json
                pass
        else:
            # Simulate server creating entity with an ID
            return {'id': randint(0, sys.maxint)}
