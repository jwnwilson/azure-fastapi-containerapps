# FastAPI with Celery

> Minimal example utilizing FastAPI and Celery with RabbitMQ for task queue, Redis for Celery backend and flower for monitoring the Celery tasks.

## Requirements

- Docker
  - [docker-compose](https://docs.docker.com/compose/install/)

## Run example

1. Run command ```docker-compose up```to start up the RabbitMQ, Redis, flower and our application/worker instances.
2. Navigate to the [http://localhost:8000/docs](http://localhost:8000/docs) and execute test API call. You can monitor the execution of the celery tasks in the console logs or navigate to the flower monitoring app at [http://localhost:5555](http://localhost:5555) (username: user, password: test).

## Run application/worker without Docker?

### Requirements/dependencies

- Python >= 3.7
  - [poetry](https://python-poetry.org/docs/#installation)
- RabbitMQ instance
- Redis instance

> The RabbitMQ, Redis and flower services can be started with ```docker-compose -f docker-compose-services.yml up```

### Install dependencies

Execute the following command: ```poetry install --dev```

### Run FastAPI app and Celery worker app

1. Start the FastAPI web application with ```poetry run hypercorn app/main:app --reload```.
2. Start the celery worker with command ```poetry run celery worker -A app.worker.celery_worker -l info -Q test-queue -c 1```
3. Navigate to the [http://localhost:8000/docs](http://localhost:8000/docs) and execute test API call. You can monitor the execution of the celery tasks in the console logs or navigate to the flower monitoring app at [http://localhost:5555](http://localhost:5555) (username: user, password: test).

# Container apps setup

Run the following in a bash shell

### Set env vars
```
export RESOURCE_GROUP="fastapi-containerapps"
export LOCATION="northeurope"
export ENVIRONMENT="env-fastapi-containerapps"
export API_NAME="fastapi-api"
export WORKER_NAME="fastapi-celery"
export FRONTEND_NAME="fastapi-ui"
export ACR_NAME="mycontainerregistrynoel"
```

### Create resource group
```
az group create \
  --name $RESOURCE_GROUP \
  --location "$LOCATION"
```

### Create container registry
```
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true
```

### Build and upload docker image
`az acr build --registry $ACR_NAME --image $API_NAME .`

### Create container app env
```az containerapp env create \
  --name $ENVIRONMENT \
  --resource-group $RESOURCE_GROUP \
  --location "$LOCATION"
```

### Deploy fastapi container
```az containerapp create \
  --name $API_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT \
  --image $ACR_NAME.azurecr.io/$API_NAME \
  --target-port 80 \
  --ingress 'external' \
  --registry-server $ACR_NAME.azurecr.io \
  --query properties.configuration.ingress.fqdn
```

# Setup redis container

### Deploy fastapi container
`az provider register --namespace Microsoft.ServiceLinker`

```az containerapp service redis create \
  --name myredis \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$ENVIRONMENT"
```
  
Get redis password from redis config and update image / env var with redis password.

### Connect fastapi container to redis container
```az containerapp update \
  --name $API_NAME \
  --resource-group $RESOURCE_GROUP \
  --image $ACR_NAME.azurecr.io/$API_NAME:v1 \
  --bind myredis
```

### Deploy celery container

I was unable to re-use the existing image and set the --command arg successfully, there isn't an example in the docs or info available on stack overflow so I created a new docker image with the celery.Dockerfile file tagged: "worker_v1"

```az containerapp create \
  --name $WORKER_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT \
  --image $ACR_NAME.azurecr.io/$API_NAME:worker_v1 \
  --registry-server $ACR_NAME.azurecr.io \
  --bind myredis
```
  
