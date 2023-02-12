from locust import HttpLocust, TaskSet


def healthCheck(l):
	response = l.client.get("/health")
  # print("Response status", response.status.code)
  # print("Response content", response.text)

def getRejectionReason(l):
  response = l.client.get("/cr2/reasons?cashbackIds[]=3192014&cashbackIds[]=21731699")
  # print("Response status", response.status.code)
  # print("Response content", response.text)

class UserBehavior(TaskSet):
    tasks = {healthCheck:1, getRejectionReason:2}

class WebsiteUser(HttpLocust):
    host = 'http://1.50.36.252'
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 1000