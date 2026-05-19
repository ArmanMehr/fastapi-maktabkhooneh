from locust import HttpUser, between, task

BACKEND_HOST = "http://backend:8000"


class QuickstartUser(HttpUser):
    host = BACKEND_HOST
    wait_time = between(1, 2)

    def on_start(self):
        self.client.post(
            "/users/login",
            json={"username": "string", "password": "stringst"},
        )

    @task
    def get_all_expenses(self):
        self.client.get("/expenses")
