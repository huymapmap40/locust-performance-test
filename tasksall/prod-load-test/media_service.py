from locust import TaskSet, task, HttpUser, between
import random
# for media service
class MediaServiceUserBehavior(TaskSet):
  def __init__(self, parent):
    super(MediaServiceUserBehavior, self).__init__(parent)

    self.list_ids = [
      [1,45,11,13,24,17,6,23,33],
      [11,26,31,7,36,29,39,40,5],
      [12,39,46,33,16,3,11,29,28],
      [18,47,19,33,44,12,48,36,31],
      [1,48,19,40,30,43,22,35,21],
      [26,11,32,23,20,7,30,47,13],
      [39,15,23,12,44,13,47],
      [38,20,39,34,12,9,29,3],
      [39,42,48,14,33,31,47,41],
      [4,29,26,11,13,38,32,40]
    ]

  @task(1)
  def fetchMedia(self):
    mediaIds = random.choice(self.list_ids)
    mediaIdsQueryString = ",".join(str(i) for i in mediaIds)
    self.client.get(
      url="http://media-service.internal.prod-sg.svc.shopback.com/v1/projects/1/media?filter=id||$in||" + mediaIdsQueryString,
    )

  @task(1)
  def fetchCollateral(self):
    querystring = {"type":"Merchant","sourceIds":"123,18708,18137,18146,19312,19355,17934,18532"}
    self.client.get(
        url='http://media-service.internal.prod-sg.svc.shopback.com/v1/collateral-default',
        params=querystring,
    )
  

class MediaServiceWebsiteUser(HttpUser):
  tasks = [MediaServiceUserBehavior]
  wait_time = between(0.1, 0.5)
