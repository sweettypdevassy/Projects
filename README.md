# Node Application Containerized with Docker and Jenkins Integration


## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Workflow](#project-workflow)
- [Setting up Docker and Jenkins](#setting-up-docker-and-jenkins)
- [Setup and Configuration](#setup-and-configuration)
- [Jenkins Pipeline](#jenkins-pipeline)
- [Email Notifications](#email-notifications)

## Overview
The "Node Application Containerized with Docker and Jenkins Integration" project showcases the process of building and containerizing a Node.js application using Docker and automating its CI/CD pipeline with Jenkins.   
The Jenkins pipeline is configured to trigger builds, create Docker images of the application, push them to Docker Hub, and send email notifications with the build results. This integration ensures a streamlined workflow for continuous integration and deployment, enhancing efficiency and reliability in the development process.  

  

## Prerequisites
To get started, ensure you have the following installed:

- Docker
- Jenkins
- Git 

## Project Workflow
1. Clone the repository.
2. Build the Docker image.
3. Run the application in a Docker container.
4. Set up a Jenkins pipeline for CI/CD.
5. Automate Docker image builds and pushes to DockerHub.


## Setting up Docker and Jenkins

Before you begin, you'll need to set up Docker and Jenkins. You can follow the official documentation for installation and configuration using Docker:

[Setting up Docker and Jenkins](https://www.jenkins.io/doc/book/installing/docker/)

Please refer to this guide for instructions. Here are the key points included in the documentation:

1. **Install Docker:**
   - The guide explains how to install Docker on various operating systems, including Linux, macOS, and Windows.
   - It includes system requirements, dependencies, and detailed installation steps.

2. **Install Jenkins with Docker:**
   - The steps for installing Jenkins using Docker are clearly explained, ensuring Jenkins runs as a Docker container.
   - The guide includes running the official Jenkins image, configuring Jenkins for the first time, and accessing through the web interface.

3. **Set Up Jenkins with Docker:**
   - Details are provided on how to set up Jenkins to use Docker and how to ensure Jenkins has access to Docker commands for building images and running containers.
   - The process of configuring Jenkins to run Docker containers securely is covered.

4. **Configure DockerHub Credentials for Jenkins:**
   - Instructions on how to store DockerHub credentials in Jenkins securely, so Jenkins can push Docker images after building them.
   
---
## Setup and Configuration

### Clone the Repository
Clone the repository containing the Node.js application:

```bash
git clone https://github.com/yourusername/nodejs-demo.git
cd nodejs-demo
```  

### Create the Docker Image
To containerize the Node.js application, build a Docker image:

```bash
docker build -t yourusername/nodeapp .
```

This will create a Docker image with the tag 
`yourusername/nodeapp`.

### Run the Application in a Docker Container

Once the image is built, run the application inside a Docker container:

```bash
docker run -d -p 3000:3000 yourusername/nodeapp
```
The application will be accessible at [http://localhost:3000](http://localhost:3000).

## Jenkins Pipeline
Automate the process of building and pushing Docker images using Jenkins. The following Jenkins pipeline script demonstrates the setup.

### Jenkins Pipeline Script (`Jenkinsfile`)
```groovy
pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
    }
    stages {
        stage('SCM Checkout') {
            steps {
                git 'https://github.com/yourusername/nodejs-demo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t yourusername/nodeapp:$BUILD_NUMBER .'
            }
        }

        stage('Login to DockerHub') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }
        stage('Push Docker Image') {
            steps {
                sh 'docker push yourusername/nodeapp:$BUILD_NUMBER'
            }
        }
    }
    post {
        always {
            sh 'docker logout'
        }
    }
}
```

### Key Steps in the Pipeline

- **SCM Checkout**: Checks out the latest code from the GitHub repository.
- **Build Docker Image**: Builds a Docker image using the `Dockerfile` and tags it with the Jenkins build number.
- **Login to DockerHub**: Logs into DockerHub using credentials stored in Jenkins.
- **Push Docker Image**: Pushes the newly built Docker image to DockerHub.

### Configure Jenkins with DockerHub Credentials
In Jenkins, configure your DockerHub credentials:
1. Go to **Manage Jenkins > Manage Credentials**.
2. Add a new credential with your DockerHub username and password.

### Running the Jenkins Pipeline

Once the pipeline is set up, every time a change is pushed to the GitHub repository, Jenkins will automatically:

1. Checkout the latest code.
2. Build a new Docker image.
3. Push the Docker image to DockerHub.

### View the Results

After a successful pipeline run:

- **Check Jenkins Console Output**: Verify that the build and push steps completed successfully.
- **View the Docker Image on DockerHub**: Log in to your DockerHub account to see the newly created image.

## Email Notifications
To ensure you are notified of the pipeline's status, configure email notifications in Jenkins. Use the **Email Notification** or **Extended Email Notification** plugins to send build results to your email address.

---






