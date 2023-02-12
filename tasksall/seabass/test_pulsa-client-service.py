from locust import HttpUser, TaskSet, task
import random


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    def getType(self):
      return random.choice([
        "pulsa"
      ])

    def getCode(self):
      return random.choice([
        "hthree25000",
        "hthree50000",
        "hthree100000",
        "hthree150000",
        "hthree200000",
        "hthree300000",
        "hsmart25000",
        "hsmart50000",
        "hsmart100000",
        "hsmart150000",
        "hsmart200000",
        "hsmart300000",
        "htelkomsel25000",
        "htelkomsel50000",
        "htelkomsel100000",
        "htelkomsel150000",
        "htelkomsel200000",
        "htelkomsel300000",
        "haxis25000",
        "haxis50000",
        "haxis100000",
        "haxis200000",
        "xld25000",
        "xld50000",
        "xld100000",
        "xld150000",
        "xld200000",
        "xld300000",
        "hindosat25000",
        "hindosat50000",
        "hindosat100000",
        "hindosat150000",
        "hindosat200000",
      ])

    @task
    def userBrowseForCashingOut(self):
        type = self.getType()
        code = self.getCode()
        self.client.get(
          url='/pricelist/'+ type + '/' + code
        )

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000