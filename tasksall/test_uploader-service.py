from locust import HttpLocust, TaskSet, task
import base64
import random
import json

# Actual service but fake endpoint
# Uploader-service will try to call but fail
SERVICE = "cashback-engine-service"
PURPOSE = "fake/endpoint/load-test"
EMAIL = "loadtest.dummy@shopback.com"

FILENAME = "uploader-service_load-test.csv"
FILEPATH = "/locust-tasks/uploader-service_load-test.csv"

class UserBehavior(TaskSet):

    def on_start(self):
        self.headers = { "Cache-Control": "no-cache" }

    @tag('view')
    @task()
    def view_uploads(self):
        queryString = "&".join(
            "service=" + SERVICE, 
            "purpose=" + PURPOSE
        )

        print("Viewing uploads: " + queryString)
        response = self.client.get(
            "/api/uploads?" + queryString, 
            headers=self.headers
        )
        print(response.text)

    @tag('upload')
    @task()
    def upload_file(self):
        presigned_payload = {
            "method": "PUT",
            "fileName": FILENAME,
            "purpose": PURPOSE,
            "service": SERVICE,
            "userEmail": EMAIL
        }

        print("1. Getting presigned url")
        presigned_response = self.client.post(
            url="/api/presigned",
            headers=self.headers,
            json=presigned_payload,
        ).json()

        # This part will actually upload to S3 (dev folder)
        print("2. Uploading using presigned url")
        presigned_url = presigned_response.presignedUrl
        presigned_headers = { "Content-Type": 'text/csv' }
        s3_response = self.client.put(
            url=presigned_url,
            headers=presigned_headers,
            data=open(FILEPATH, "rb")
        )

        # Inside uploader-service, this part moves the S3 file
        # And moves on to "process" the upload (by calling related service)
        print("3. Telling uploader-service that upload is done")
        upload_id = presigned_response.uploadId
        update_upload_payload = {
            id: upload_id,
            status: "Uploaded"
        }
        update_upload_response = self.client.post(
            url="/api/uploads",
            headers=self.headers,
            json=update_upload_payload
        )
        print("Update complete: " + update_upload_response.text)


class NeedleUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 500
