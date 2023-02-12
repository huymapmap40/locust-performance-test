import logging
from pydoc import resolve
from urllib import response
from locust import HttpUser, TaskSet, task, between
import random

class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.client.verify = False

    @task
    def requestRedirectPage(self):
        webAffiliateLinkIds = [67780, 219859, 186986, 219887, 216857, 159415]
        affiliateLinkId = random.choice(webAffiliateLinkIds)

        headers = {
            'x-shopback-context-redirect': '{"affiliateId":"' + str(affiliateLinkId) + '"}',    
            'x-shopback-context-useragent': '{"isIE":false,"source":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36","isMobile":false,"isTablet":false,"isAndroid":false,"browserName":"Chrome","browserVersion":"103.0.0.0","browserPlatform":"Apple Mac","isIOS":false}',
            'x-shopback-context-user': '{"id":3680043,"uuid":"c4347c4d578b48d9a8733239bb4c5b79","firstName":"","lastName":"","dob":-1,"email":"nason@shopback.com","overview":{"cashbackPending":0,"cashbackAffiliatePaid":0,"moneybagBalance":0,"userWithdrawalTotal":0,"updatedAt":""},"guid":"c4347c4d578b48d9a8733239bb4c5b79-4","type":"","jwtToken":"ZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFkV2xrSWpvaVl6UXpORGRqTkdRMU56aGlORGhrT1dFNE56TXpNak01WW1JMFl6VmlOemtpTENKcGMzTWlPaUozZDNjdWMyaHZjR0poWTJzdWNHZ2lMQ0pwYzNOMVpXUkJkQ0k2TVRZMU9UVXpPREk0TWk0ek9UY3NJbk5qYjNCbElqcGJJbEpGUVVRaUxDSlhVa2xVUlNKZExDSnlaV1p5WlhOb1ZHOXJaVzVKWkNJNklqWXlaV0UwT0dOaFkyTXpOMkpoTURBd09HTXdaVFZpWmlJc0ltbGhkQ0k2TVRZMU9UVXpPREk0TWl3aVpYaHdJam94TmpVNU5UUXhPRGd5ZlEuYnJpNC12N3B6VC1xNW9MdnVXdXh2LU15dVlCd3NKdlpGaWc3cHpNTEw4ZnlqUHFHQVkteFVVMUhRVldfRTRHSld0dkluUGxYVDR3WWI2SUhRejRzQVR3dGY3cmVYcnNXaHl2TzVtSzVIR3NsczNpblFzenJfa0VPcnZuc1VfRHdlcHZ4VHpoQURyc1l0T0tSMkhCTWgyUWplSDMycGppbGppRVNQSjVYX25nbUZ5QVlEbFdJWmU5Z2xJdWt4SE5qUHVxeVdUV0Y1NE1POEJWQVpoeFpJVlBnS1BiemZfUHA1SVU5QUF1NS00MFFzbnRVelJSUmM2aThKQkd1V2NhdlBFWGZEcjZGTXRBcW91ZWI4ck50Nm41WGR4Z1hhNzRGNVl0RXBTWmR4RW52dFZDa3BzRnJsMEp0bXZXaUFVSUx0UWYyQy0yRVZ3S1VVY0lLWkRKZ29R","isMobileNumberVerified":false,"isEmailVerified":false,"isNiceVerified":false,"kycSummary":"NONE"}',
            'x-shopback-context-client': '{"entryUrl":"http://localhost:8080","ipAddress":"::1","referrerUrl":"https://staging.shopback.ph/redirect/alink/' + str(affiliateLinkId) + '"}',
            'x-shopback-context-param': '{"path":"/redirect/alink/' + str(affiliateLinkId) + '","query":{},"params":{}}'
        }

        with self.client.get(
            url='/redirect',
            headers=headers
        ) as response:
            if response.status_code == 200:
                logging.info('success!')
            else:
                logging.info('fail -> %s', response.status_code)
        self.client.close()

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(0.3, 0.8)

