from locust import HttpUser, TaskSet, task, between
import random

class UserBehavior(TaskSet):
    def on_start(self):
        i = random.randint(1, 10000)
        self.email = f"user{i}@example.com"
        self.password = "password123"

        self.client.post(
            "/register",
            data={
                "name": f"User {i}",
                "email": self.email,
                "password": self.password,
                "password_confirm": self.password,
            },
            allow_redirects=False
        )

        self.client.post(
            "/login",
            data={
                "username": self.email,
                "password": self.password,
            },
            allow_redirects=True
        )

        self.todo_ids = []

    def on_stop(self):
        self.client.get("/logout", allow_redirects=True)

    @task(3)
    def create_todo(self):
        content = f"Task {random.randint(1, 10000)}"
        response = self.client.post(
            "/todo",
            data={"content": content},
            allow_redirects=False
        )

        # Capture item_id from response if returned as JSON
        try:
            todo_data = response.json()
            if "id" in todo_data:
                self.todo_ids.append(todo_data["id"])
            else:
                # Fallback: generate a random id if API does not return it
                self.todo_ids.append(random.randint(1, 10000))
        except Exception:
            # If response is not JSON, fallback to random id
            self.todo_ids.append(random.randint(1, 10000))

    @task(2)
    def update_todo(self):
        if not self.todo_ids:
            return
        item_id = random.choice(self.todo_ids)
        is_complete = random.choice([True, False])
        self.client.put(
            f"/todo/{item_id}",
            json={"is_complete": is_complete},
            allow_redirects=False
        )

    @task(1)
    def delete_todo(self):
        if not self.todo_ids:
            return
        item_id = self.todo_ids.pop(0)
        self.client.delete(
            f"/todo/{item_id}",
            allow_redirects=False
        )

    @task(2)
    def dashboard_view(self):
        search_query = random.choice(["", "task", "example"])
        self.client.get(f"/dashboard?search={search_query}",)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
