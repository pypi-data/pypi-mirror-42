# SLA Monitor Worker

This is the test runner portion of the SLA monitor/reporter. It performs tests (or any command you want) repeatedly, and publishes success/failure to an SNS topic for external processing (for example, using lambda to write to a custom cloudwatch metric), as well as optionally uploading logs to an S3 bucket.

## Installing

To install simply install via pip

```bash
pip install --user sla-runner
```

Highly recommended is iam-docker run:

```bash
pip install --user iam-docker-run
```

This project assumes you are using role based authentication, as would be used in a production environment in AWS. This mimics that environment by running with an actual role.

## Terraform

Excute 

```shell
# pip install iam-starter
cd terraform && \
export AWS_ENV="dev" && \
export AWS_DEFAULT_REGION="us-east-1" && \
iam-starter \
    --profile $AWS_ENV \
    --command "terraform init && terraform apply \
        --auto-approve \
        -var \"aws_env=$AWS_ENV\" \
        -var \"aws_region=$AWS_DEFAULT_REGION\""
```

## Using

Use iam-docker-run outside of AWS to run tests. In real life scenarios on ECS, instead install sla-runner via pypi in your service container, and set `--image` to the image of the service container which contains your test.

```bash
docker build -t sla-monitor/sla-runner:latest .

export AWS_ENV="dev"
iam-docker-run \
    -e "SLARUNNER_COMMAND='/bin/bash /src/test-scripts/run-tests.sh'" \
    -e "SLARUNNER_SERVICE=example-service" \
    -e "SLARUNNER_GROUPS='dev-team,critical'" \
    -e "SLARUNNER_DELAY=30" \
    -e "SLARUNNER_SNSTOPICARN='arn:aws:sns:us-east-1::sla-monitoring-worker-$AWS_ENV'" \
    -e "SLARUNNER_S3BUCKETNAME='sla-monitoring-logs-$AWS_ENV'" \
    --full-entrypoint "sla-runner" \
    --region us-east-1 \
    --profile $AWS_ENV \
    --role sla-monitor-runner-role-$AWS_ENV \
    --image sla-monitor/sla-runner:latest
```

iam-docker-run loads a custom env file (`iam-docker-run.env`) to prevent long commands like that. In ECS, add these as environment variables in the task definition or load from ssm via ssm-starter:

```
--full-entrypoint "ssm-starter --ssm-name slarunner --command 'sla-runner'"
```

## Variables

The runner takes the following values which are provided by environment variable. 

#### command

$SLARUNNER_COMMAND

Command to be run repeatedly. Pretty straightforward. If there is an interrupt, the runner will attempt to finish the command gracefully before exit.

#### service

$SLARUNNER_SERVICE

Name of the component service you're testing. This will be used as the prefix for s3 uploads, and will be passed in the JSON event as "service" to SNS.

#### groups

$SLARUNNER_GROUPS

Name of the grouping of components you're testing, in csv format. This will be passed in the JSON event as "groups" to SNS as a list, and is meant to provide secondary statistics if multiple services are part of the same component.

#### delay

$SLARUNNER_DELAY

How long to wait between commands being run in seconds.

#### sns-topic-arn

$SLARUNNER_SNSTOPICARN

SNS topic arn to publish results to. It will be published as a JSON object. For example, the command above would produce the following:

```json
{
    "service": "example-service",
    "group": ["dev-team", "critical"],
    "succeeded": true,
    "timestamp": "1574514000",
    "testExecutionSecs": "914" #seconds
}
```

#### s3-bucket-name

$SLARUNNER_S3BUCKETNAME

Bucket to write logs to. This is an optional parameter. The object will be named as the timestamp followed by the result for easily searching by result, and will be prefixed by the service name. For example "example-service/1574514000_SUCCESS"

## Development and Testing

```bash
docker build -t sla-runner:latest -f Dockerfile .
```

```bash
iam-docker-run \
    --image sla-runner:latest \
    --role sla-monitor-runner-role \
    --profile dev \
    --host-source-path . \
    --container-source-path /src
    --full-entrypoint "/bin/bash"
```

You will need to run `pip install -e .` again once you're in to live link the code.

## Publishing Updates to PyPi

For the maintainer - to publish an updated version of ssm-search, increment the version number in version.py and run the following:

docker build -f ./Dockerfile.buildenv -t sla-runner:build .
docker run --rm -it --entrypoint make sla-runner:build publish

At the prompts, enter the username and password to the pypi.org repo.