"""
:Authors:
    yauritux <yauri.attamimi@moove.io>
"""
import json

from locust import HttpUser, SequentialTaskSet, task, constant, tag
from util.csvreader import CsvRead


class DriverApp(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.access_token = None
        self.username = None

    @task
    @tag("story", "login")
    def post_login(self):
        test_data = CsvRead("staging/data.csv").read()

        print(f"login::test_data {test_data}")

        name = "Login for " + test_data["username"]
        self.username = test_data["username"]

        with self.client.post(
                url="/user/login", catch_response=True, name=name,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                data=json.dumps({
                    "username": test_data["username"],
                    "pin": test_data["pin"],
                    "device_id": test_data["device_id"]
                })
        ) as response:
            if response.status_code == 200:
                self.access_token = response.json().get("access_token")
                print(self.access_token)
                response.success()
            elif response.status_code == 400:
                error_msg = response.json().get("error")
                print(error_msg)
                self.reset_driver_data()
                response.success()
            elif response.status_code == 401:
                error_msg = response.json().get("error")
                print(error_msg)
                self.reset_driver_data()
                response.success()
            elif response.status_code == 403:
                error_msg = response.json().get("error")
                print(error_msg)
                self.reset_driver_data()
                response.success()
            else:
                self.reset_driver_data()
                if "error" in response.json():
                    response.failure(f"Error with message {response.json().get('error')}")
                else:
                    response.failure(f"Error with status code {response.status_code}")

    @task
    @tag("story")
    def get_basic_profile(self):
        if self.access_token is None:
            return

        print(f"get driver basic profile for token {self.access_token}")
        name = f"Get {self.username} Basic Profile"
        with self.client.get(url="/profile/api/v1/basic", name=name, catch_response=True,
                             headers={
                                 "Content-Type": "application/json",
                                 "Accept": "application/json",
                                 "Authorization": f"Bearer {self.access_token}"
                             }) as response:
            if response.status_code == 200:
                print(f"{response.status_code}: {response.text}")
                response.success()
            else:
                if "error" in response.json():
                    response.failure(f"Error with message {response.json().get('error')}")
                else:
                    response.failure(f"Error with status code {response.status_code}")

    @task
    @tag("story")
    def get_sensitive_profile(self):
        if self.access_token is None:
            return

        print(f"get driver basic profile for token {self.access_token}")
        name = f"Get {self.username} Sensitive Profile"
        with self.client.get(url=f"/profile/{self.username}/sensitive", name=name, catch_response=True,
                             headers={
                                 "Content-Type": "application/json",
                                 "Accept": "application/json",
                                 "Authorization": f"Bearer {self.access_token}"
                             }) as response:
            if response.status_code == 200:
                print(f"{response.status_code}: {response.text}")
                response.success()
            else:
                if "error" in response.json():
                    response.failure(f"Error with message {response.json().get('error')}")
                else:
                    response.failure(f"Error with status code {response.status_code}")

    @task
    @tag("story")
    def get_driver_image(self):
        if self.access_token is None:
            return

        print(f"get driver image for token {self.access_token}")
        name = f"Get {self.username} Image"
        with self.client.get(url=f"/profile/api/v1/image", name=name, catch_response=True,
                             headers={
                                 "Content-Type": "application/json",
                                 "Accept": "application/json",
                                 "Authorization": f"Bearer {self.access_token}"
                             }) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error with status code {response.status_code}")

    @task
    @tag("story")
    def get_driver_plan_performance(self):
        if self.access_token is None:
            return

        print(f"get driver plan performance for token {self.access_token}")
        name = f"Get {self.username} Plan Performance"
        with self.client.get(url="/asset/plan/performance", name=name, catch_response=True,
                             headers={
                                 "Content-Type": "application/json",
                                 "Accept": "application/json",
                                 "Authorization": f"Bearer {self.access_token}"
                             }) as response:
            if response.status_code == 200 or response.status_code == 204:
                print(f"{response.status_code}: {response.text}")
                response.success()
            else:
                if "error" in response.json():
                    response.failure(f"Error with message {response.json().get('error')}")
                else:
                    response.failure(f"Error with status code {response.status_code}")

    @task
    @tag("story", "unread_notifications")
    def get_unread_notifications(self):
        if self.access_token is None:
            return

        print(f"get driver unread notification for token {self.access_token}")
        name = f"Get {self.username} unread notifications"
        with self.client.get(url="/notification/list/unread", name=name, catch_response=True,
                             headers={
                                 "Content-Type": "application/json",
                                 "Accept": "application/json",
                                 "Authorization": f"Bearer {self.access_token}"
                             }) as response:
            if response.status_code == 200:
                print(f"{response.status_code}: {response.text}")
                response.success()
            else:
                if "error" in response.json():
                    response.failure(f"Error with message {response.json().get('error')}")
                else:
                    response.failure(f"Error with status code {response.status_code}")

    @task
    @tag("driver_status")
    def get_driver_status(self):
        test_data = CsvRead("staging/data.csv").read()
        print(f"get_driver_status::test_data {test_data}")

        name = "Get Driver Status for " + test_data["username"]
        username = test_data["username"]
        with self.client.get(url=f"/user/{username}/moove/status", name=name, catch_response=True) as response:
            if response.status_code == 200:
                print(f"{response.status_code}: {response.text}")
                response.success()
            else:
                if "error" in response.json():
                    response.failure(f"Error with message {response.json().get('error')}")
                else:
                    response.failure(f"Error with status code {response.status_code}")

    def reset_driver_data(self):
        self.access_token = None
        self.username = None


class PerformanceTest(HttpUser):
    host = "https://stage.api.moove.link"
    wait_time = constant(1)
    tasks = [DriverApp]
