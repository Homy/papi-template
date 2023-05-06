# API Test Framework

This is a Python-based API test framework that uses pytest and requests libraries to run automated tests against RESTful APIs. It also integrates with TestRail to report test results.

## Setup

To use this framework, you'll need to have Python 3.x installed on your system. You can install all required dependencies by running:

```
pip install -r requirements.txt
```

Next, you'll need to create a `config.ini` file with the following information:

- API base URL
- TestRail API endpoint
- TestRail username and password
- TestRail project ID
- TestRail test suite ID
- TestRail test case custom field name (optional)

## Running Tests

To run tests, navigate to the project directory and run:

```
pytest tests/
```

By default, tests will run against the production environment. To specify a different environment, use the `--env` flag followed by the environment name:

```
pytest tests/ --env staging
```

To run specific tests, use the `-k` flag followed by the test name:

```
pytest tests/ -k test_get_request
```

## Reporting Results to TestRail

To report test results to TestRail, you'll need to add a TestRail test case ID to each test case in the format `C###` (e.g. `C123`). You can also add a TestRail test case custom field value to each test case using the `custom_field` fixture.

When tests are run, results will be automatically posted to TestRail using the provided API credentials. Test cases that don't have a matching ID in TestRail will be skipped.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
