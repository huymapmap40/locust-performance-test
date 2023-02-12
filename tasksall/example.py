from locust import HttpUser, TaskSet, task

class ElbTasks(TaskSet):
  @task
  def status(self):
      self.client.get("/status")

class ElbWarmer(HttpUser):
  tasks = [ElbTasks]
  min_wait = 1000
  max_wait = 3000
