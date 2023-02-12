from locust import HttpUser, TaskSet
import requests
import time
import random

# dns_list_fn = 'dns_list.txt'  # path for local
dns_list_fn = '/locust-tasks/dns_list.txt'  # path for k8s

with open(dns_list_fn, 'r') as f:
    dns_list_org = f.read().splitlines()

dns_list = []
for hostname in dns_list_org:
    if '#' not in hostname:
        dns_list.append(hostname)

def getRoot(l):
    curlDnsResolve(l=l, method="GET")

def postRoot(l):
    curlDnsResolve(l=l, method="POST")
 
class UserBehavior(TaskSet):
    tasks = {getRoot:1}
    # tasks = {postRoot:1}
 
class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 0
    max_wait = 0

def curlDnsResolve(l=None, hostname=None, method=None):
    if hostname is None:
        hostname = random.choice(dns_list)
    if l:
        if method == "GET":
            l.client.get("/?hostname=%s" % hostname)
        elif method == "POST":
            l.client.post('/', json={"hostname": hostname})
    else:
        if method == "GET":
            return requests.get('http://localhost:8080/?hostname=%s' % hostname)
        elif method == "POST":
            return requests.post('http://localhost:8080/', json={"hostname": hostname})        

if __name__ == "__main__":
    hostname = random.choice(dns_list)
    res = curlDnsResolve(hostname=hostname, method="POST")
    print(res.json())