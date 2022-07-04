from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def landing(self):
        response = self.client.get("/")

    @task
    def login(self):
        response = self.client.post("/showSummary", {"email": "Iron Temple"})

    @task
    def logout(self):
        response = self.client.get("/logout")

    @task
    def booking(self):
        response = self.client.get("/book/Fall Classic/She Lifts")

    @task(2)
    def purchase(self):
        form = {"competition": "Fall Classic",
                "club": "She Lifts",
                "places": "12"}
        response = self.client.post("/purchasePlaces", form)
