import pytest
import requests
import json
import xml.etree.ElementTree as ET
from testrail import *
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Load TestRail credentials from the config file
client = APIClient(config['TESTRAIL']['url'])
client.user = config['TESTRAIL']['email']
client.password = config['TESTRAIL']['token']
project_id = config.getint('TESTRAIL', 'project_id')
suite_id = config.getint('TESTRAIL', 'suite_id')
section_id = config.getint('TESTRAIL', 'section_id')

@pytest.fixture
def case(request):
    return request.node.name

@pytest.fixture
def tr_case_id(request, case):
    response = client.send_get(f"get_cases/{project_id}&suite_id={suite_id}&section_id={section_id}")
    for tr_case in response:
        if tr_case['title'] == case:
            return tr_case['id']

@pytest.fixture
def tr_status(request):
    tr_status = None
    outcome = request.node.rep_call.outcome
    if outcome == 'passed':
        tr_status = 1
    elif outcome == 'failed':
        tr_status = 5
    return tr_status

def pytest_sessionfinish(session, exitstatus):
    if exitstatus == pytest.ExitCode.OK:
        client.send_post(f"close_run/{client.send_get(f"get_runs/{project_id}&is_completed=0&suite_id={suite_id}")[0]['id']}", {'status_id': 1})
    else:
        client.send_post(f"close_run/{client.send_get(f"get_runs/{project_id}&is_completed=0&suite_id={suite_id}")[0]['id']}", {'status_id': 5})

@pytest.fixture
def url():
    return config['API']['base_url']

@pytest.fixture
def endpoint():
    return config['API']['endpoint']

@pytest.fixture
def params():
    return config['API']['params']

@pytest.fixture
def headers():
    return json.loads(config['API']['headers'])

@pytest.fixture
def response(url, endpoint, params, headers):
    response = requests.get(url + endpoint, params=params, headers=headers)
    response_json = response.json()
    if response.status_code == 200:
        return {"status": "success", "code": response.status_code, "data": response_json}
    else:
        return {"status": "failure", "code": response.status_code, "data": response_json}

def test_api_returns_200_status_code(response, tr_case_id, tr_status):
    assert response["status"] == "success"
    assert response["code"] == 200

    # Report test results to TestRail
    client.send_post(f"add_result_for_case/{client.send_get(f"get_runs/{project_id}&is_completed=0&suite_id={suite_id}")[0]['id']}/{tr_case_id}", {'status_id': tr_status})


def test_api_returns_json_response(response, tr_case_id, tr_status):

    assert isinstance(response["data"], list)

    # Report test results to TestRail

    client.send_post(f"add_result_for_case/{client.send_get(f"get_runs/{project_id}&is_completed=0&suite_id={suite_id}")[0]['id']}/{tr_case_id}", {'status_id': tr_status})

def test_api_returns_xml_response(url, params, headers, tr_case_id, tr_status):

    response = requests.get(url + "/posts", params=params, headers=headers)

    response_xml = ET.fromstring(response.text)

    assert response.status_code == 200

    assert response_xml.tag                   
