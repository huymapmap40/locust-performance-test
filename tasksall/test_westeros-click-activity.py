from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.client.verify = False

        self.cookies = dict(
            sbet='ZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFkV2xrSWpvaU4wRkVNRFkxUWprek5EWkNORGMzT0RnMU1qWTRNMEV6UWpJeE1FTXlRVEVpTENKcGMzTWlPaUozZDNjdWMyaHZjR0poWTJzdWMyY2lMQ0pwYzNOMVpXUkJkQ0k2TVRZeU56VTJOelF5Tmk0d01ERXNJbk5qYjNCbElqcGJJbEpGUVVRaUxDSlhVa2xVUlNKZExDSnlaV1p5WlhOb1ZHOXJaVzVKWkNJNklqWXdabUU1TldNMVpUZGhOelkzTm1aa00ySXdOV0V6TUNJc0ltbGhkQ0k2TVRZeU56VTJOelF5Tml3aVpYaHdJam94TmpJM05UY3hNREkyZlEuZkk2NVpESFlGNjhMSHptREFTclJjUkQ4Z19qb0VtcnduUDNTU3dBSmZHMUJxM2NLaU05RlNQQ0Q3Tkx5Y2N4NVB3QjBtQlZFdFBqWllnUjhZVHZaN1hESEJnS1VtTVhoQTBzZE8yWkI1bF9lbGFnQjVHdU1lN0g0Y0o1ckMtX01qbHEtSFdJSnVoR0VBRVpDRDR5bzl2MHZBRWlnR3YweXdrR0xFVzM2WlgyOXVMNEoySmtOWmZmckxSRDN6N1dtOXlLeklKdGZzZEJQSkNGUl9WdWpyd2ZERHAzdlF3RHQ4TmZXaU02QmxNeXE5NlRpZDVBS1JjYTE1WUhucWlrYkRmT21fSXhDNmlGVDhOa0NJTUNmUm1scWFLQ3c3SmF1b2xzWDM3SU9mOWtqVlo0STVVOUs1LWkxNlFJZ2pwMG5za3NXS2pDUnhyT2lCdDRhMXQ5MmRn',
            sbrefresh='c2a674b8acc883aaa6b92142c88a74f9%3Afe1f38937a5b084cb3e1afd25c86706eea636571260977afa771580b0960941ac8d9722bd7a9b221c4131cd785398ecf',
            sbaccess='9b1f5e33c38082488a28bc7487ed8c08:83be230e9ee887b2b7e3dd61bf176f86b26437ff34cef96e36dcb0947a069422d7a1820a9ac0936cf07430e8e87e9492',
            sbcookie='s%3AhXMqRxA7SXrfCN88Zg5OnSlv1Q8EBifq.QOgm79Jz6n780FUrmvenKHHJ9xulV49doKXItSy6HSA'
        )

    @task
    def requestClickActivityPage(self):
        slug = '/click-activity'
        with self.client.get(
            url=slug,
            allow_redirects=False,
            cookies=self.cookies,
            catch_response=True
        ) as response:
            print(response.history, response.status_code)
            response.success()

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(0.3, 0.8)

