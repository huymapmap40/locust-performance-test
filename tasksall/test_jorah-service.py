from locust import HttpUser, TaskSet


def lateValidation(l):
    response = l.client.get("/late-validation/enquiries?cashbackIds=13505274,13467866,13513289,13513289,13512818,13534372,13502440,13462759,13462758", headers={"X-Shopback-Agent":"sbconsumeragent/1.0", "X-Shopback-Internal":"682a46b19b953306c9ee2e8deb0dc210", 'Authorization': 'Bearer ZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFkV2xrSWpvaVltSXhPRGt3WmpNM09XWTRORGd3T1dKak5HUXdOVGc0WVRWaFlUY3pNVFVpTENKcGMzTWlPaUozZDNjdWMyaHZjR0poWTJzdVkyOXRJaXdpYVhOemRXVmtRWFFpT2pFMU5qVXlNemN5TmpVdU56TTFMQ0pwWVhRaU9qRTFOalV5TXpjeU5qVXNJbVY0Y0NJNk1UVTJOemd5T1RJMk5YMC5IUkl3V1hYXzVTc3FqanpGbmN4WWZwUG4wWVYxd1g3RnhJY3hKX0w3ZlNMT2FFSEFJZEFRRjk0bk5pMnc3ZVUzOEoyQjlTQzZWOUVjaDJ0Y3JKcHc0U1E0dlNmY1dYemszaV9vd3BpbTJJLVp2OF9LX2l4ZXptZDVCTU5JUF80Vng1UU5iS282M0F4ZkpzUVpOTXZHcFNiOUxvcmd1X3ZUczN4czVSS2VTczBlcFgyS2dHY05NTWVJQTlNQ09RNldXYnRzeXZQdzFJYnBGcVpNemdTM3o0YzRyUjdLdlFST3ZLS3NkTVNnU2FBNENTTkVWbjdrVG9aZVVnNng4c0QtUFVwVXdRTmxxcG11UVQwT29icG5XdWY2ZVpKZFEzbW16YUtVNnUzbFFCVGJxOHBma0g3YnRrZmY3aHh6XzBVVDlmT3lOVGYtSDhaNG9ackR6VTRtdXc='})
    if response.status_code == 200:
        print("Success")


def visitedStores(l):
    response = l.client.get("/missing-cashback/visited-stores?accountId=3755109")
    if response.status_code == 200:
        print("Success")


class UserBehavior(TaskSet):
    tasks = { lateValidation: 1 }


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000