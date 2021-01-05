AH Delivery Checker checks AH website and post available delivery slots to a slack channel.

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
