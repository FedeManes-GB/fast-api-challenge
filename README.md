# USER MANAGEMENT

## Description

This project provides a simple API to manage users using FastAPI. You can create, update, retrieve, and delete users from a SQLITE database.

---

## Requirements

- Python 3.x (for running locally) 
- Docker (optional)

## Running Aplication with Docker

```bash
docker build -t img-name .
docker run -p 8000:8000 img-name
```
This will run the app locally at http://0.0.0.0:8000

## Running Aplication Local

*check you are at the root level of the project*
```bash
pip install -r requirements.txt
uvicorn crud_challenge.main:app --reload
```
This will run the app locally at http://localhost:8000

## API Endpoints

### GET /users
**Description:** Retrieves a list of all users.

***Example Request:***
`GET http://localhost:8000/users`

***Example Response:***
```JSON
[
  {
    "id": 1,
    "username": "fede1234",
    "email": "fede1234@gmail.com",
    "first_name": "Federico",
    "last_name": "Test",
    "role": "admin",
    "active": true,
    "created_at": "2025-04-20T03:08:07.047076",
    "updated_at": "2025-04-20T03:08:07.047080"
  },
  ...
]
```

### GET /users/:id
**Description:** Retrieves user by ID.

***Example Request:***
`GET http://localhost:8000/users/1`

***Example Response:***
```JSON
{
    "id": 1,
    "username": "fede1234",
    "email": "fede1234@gmail.com",
    "first_name": "Federico",
    "last_name": "Test",
    "role": "admin",
    "active": true,
    "created_at": "2025-04-20T03:08:07.047076",
    "updated_at": "2025-04-20T03:08:07.047080"
}
```

### POST /users/create
**Description:** Creates a new user to database.

***Example Request:***
`POST http://localhost:8000/users/create`

***Example Body:***
```JSON
{
  "username": "newuser123",
  "email": "newuser123@gmail.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "active": true
}
```

***Example Response:***
```JSON
{
    "id": 2,
    "username": "newuser123",
    "email": "newuser123@gmail.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "active": true,
    "created_at": "2025-04-20T03:08:07.047076",
    "updated_at": "2025-04-20T03:08:07.047080"
}
```

### PUT /users/update/:id
**Description:** Updates a specific ID user with new data.

***Example Request:***
`POST http://localhost:8000/users/update/1`

***Example Body:***
```JSON
{
  "username": "updated",
}
```

***Example Response:***
```
status_code = 204 No Content
```

### DELETE /users/delete/:id
**Description:** Deletes a specific user by ID.

***Example Request:***
`POST http://localhost:8000/users/delete/1`

***Example Response:***
```JSON
status_code = 204 No Content
```

## API Documentation

FastAPI automatically generates interactive documentation for this API by using Swagger and Redoc. This documentation can be accessed at:

**Swagger:** `http://0.0.0.0:8000/docs or http://localhost:8000/docs`  
**Redoc:** `http://0.0.0.0:8000/redoc or http://localhost:8000/redoc`

Additionally, we can view the OpenAPI schema at:

`http://0.0.0.0:8000/openapi.json or http://localhost:8000/openapi.json`

## Testing
This app contains a Test folder. By running at the root level of the project the test cases we can monitore the functionality of the app.

```bash
pytest -v
```

## Google Cloud Deployment

Este proyecto utiliza **Google Cloud Build**, **Docker**, y **Cloud Run** para crear, construir y desplegar la aplicación de manera eficiente y escalable. A continuación, se explica el flujo de trabajo que sigue el archivo `cloudbuild.yaml`, el cual define el proceso de construcción y despliegue automático.

### Application Deployment on Google Cloud

This project uses **Google Cloud Build**, **Docker**, and **Cloud Run** to efficiently and scalably build, containerize, and deploy the application. Below is an explanation of the workflow defined in the `cloudbuild.yaml`, which automates the build and deployment process.

### Google Cloud Build Workflow

The `cloudbuild.yaml` file defines a series of automated steps for building and deploying the application on Google Cloud. Each step is executed sequentially in Google Cloud Build.

### Steps in `cloudbuild.yaml`

1. **Verify or Create Artifact Registry Repository**

    This step checks if the **Artifact Registry** repository exists. If it doesn't, it creates one.

    ```yaml
    - name: gcr.io/google.com/cloudsdktool/cloud-sdk
    entrypoint: bash
    args:
    - "-c"
    - |
      if ! gcloud artifacts repositories describe fast-api-challenge --location=us-central1; then
        echo "Creating Repository..."
        gcloud artifacts repositories create fast-api-challenge \
        --repository-format=docker \
        --location=us-central1 \
        --description="Repo for FastAPI"
      else
        echo "Repository already exists"
      fi
    ```

2. **Build the Docker Image**
    In this step, we build the Docker image using the Dockerfile in the current directory. The image is tagged with the Artifact Registry repository

    ```yaml
    - name: 'gcr.io/cloud-builders/docker'
    args: [
      'build', '-t', 'us-central1-docker.pkg.dev/$PROJECT_ID/fast-api-challenge/app', '.'
    ]
    ```
    
3. **Run Test Before Pushing the Image**
    Before pushing the Docker image to the Artifact Registry, it is essential to run tests to ensure the application works as expected. In this step, we execute pytest inside the built Docker container to check for any issues in the code.

    ```yaml
      - name: 'gcr.io/cloud-builders/docker'
        args: ['run', '--rm', 'us-central1-docker.pkg.dev/$PROJECT_ID/fast-api-challenge/app', 'pytest', '-v']
    ```

4. **Push the Image to the Repository**
    Once the test have passed, the image is to pushed to the Artifact Registry repository.

    ```yaml
      - name: 'gcr.io/cloud-builders/docker'
        args: ['push', 'us-central1-docker.pkg.dev/$PROJECT_ID/fast-api-challenge/app']
    ```

5. **Deploy the Application to Google Cloud Run**
    With the Docker image stored in Artifact Registry, the next step is to deploy it to Google Cloud Run. Cloud Run is a fully managed service that runs Docker containers in a serverless environment.

    ```yaml
      - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
        args: [
          'run', 'deploy', 'fastapi-app',
          '--image', 'us-central1-docker.pkg.dev/$PROJECT_ID/fast-api-challenge/app',
          '--platform', 'managed',
          '--region', 'us-central1',
          '--allow-unauthenticated'
        ]
    ```

### Running `cloudbuild.yaml`
In the steps above, we used the $PROJECT_ID environment variable to point to the correct Google Cloud project.
Therefore, we need to run in terminal:
  
```bash
gcloud builds submit --config cloudbuild.yaml . --substitutions _PROJECT_ID="MY_PROJECT_ID"
```
