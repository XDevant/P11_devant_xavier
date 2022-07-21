from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def landing(self):
        self.client.get("/")

    @task
    def login(self):
        self.client.post("/showSummary", {"email": "Iron Temple"})

    @task
    def booking(self):
        self.client.get("/book/Fall Classic/She Lifts")

    @task(2)
    def purchase(self):
        form = {"competition": "Fall Classic",
                "club": "She Lifts",
                "places": "12",
                "test": "True"}
        self.client.post("/purchasePlaces", form)

    @task
    def ranking(self):
        self.client.get("/ranking")
