AH Delivery Checker checks AH website and post available delivery slots to a slack channel via [slack webhook](https://api.slack.com/messaging/webhooks).
It uses [playwright](https://github.com/microsoft/playwright-python) to visit the website and get relevant cookies, before issuing the api call.

### Run locally
To run locally, use the following command and replace the environment variables with yours:
```
docker build -t ah-checker .
docker run -it -e SLACK_WEB_HOOK=https://hooks.slack.com/services/foobar \
    -p 8080:8080 -e "SLACK_CHANNEL=#random" -e POSTCODE=1234AB -e HOUSENUMBER=101 ah-checker
```

In another shell, simply issue a GET request:
```
curl http://127.0.0.1:8080
```

Then you'll receive the available slots in your slack channel.

### Run in Google Cloud Run
Here's my setup in Cloud Run:
* Run the container as a Cloud Run service
* Use Cloud Scheduler to send message to Pub/Sub every 10 minutes
* Connect Pub/Sub with Cloud Run to trigger it to run

### TODOs
- [x] Auto deploy to cloud run.
- [ ] Capture cloud run setup in terraform.
