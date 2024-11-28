# E-Commerce Project with DevOps Implementation

## Table of Contents
1. [Overview](#overview)  
2. [Project Structure](#project-structure)  
3. [Technologies Used](#technologies-used)  
4. [Features](#features)  
5. [DevOps Workflow](#devops-workflow)  
   - [Pipeline Stages](#pipeline-stages)  
6. [Installation & Usage](#installation--usage)  
   - [Local Installation](#local-installation)  
   - [Docker Installation](#docker-installation)  
7. [Dockerfile Example](#dockerfile-example)  
8. [GitHub Actions Workflow Example](#github-actions-workflow-example)  
9. [Future Works](#future-works)  
10. [Reflections](#reflections)  
11. [References](#references) 

## Overview
This project demonstrates the development of a Django-based e-commerce platform using DevOps principles to address the challenges of monolithic architectures. The project integrates modern development practices such as modular architecture, automation, CI/CD pipelines, and advanced deployment workflows.



## Project Structure
- `.dockerignore`: Specifies files and directories to ignore during Docker builds.
- `.github/`: Contains workflows for CI/CD pipelines using GitHub Actions.
- `Dockerfile`: Configuration file for containerizing the application.
- `e_commerce/`: Core application module implementing the Model-View-Template (MVT) architecture.
- `manage.py`: Entry point for managing the Django application (e.g., migrations, development server).
- `requirements.txt`: Lists dependencies for the project.
- `stores/`: Manages store and product functionalities.
- `theme/`: Frontend themes, designed with Tailwind CSS for a clean and responsive user interface.



## Technologies Used
- **Frontend**: Tailwind CSS for styling.
- **Backend**: Django framework with Model-View-Template (MVT) architecture.
- **Database**: SQLite for lightweight and easy database management.
- **DevOps**: Docker for containerization, GitHub Actions for CI/CD, render built-in was used for monitoring.
- **Deployment**: Render for hosting production-ready applications.
- **Version Control**: Git for source code management.



## Features
1. **Authentication**:
   - User Login and Registration.
2. **Product Management**:
   - Add, Remove, and View Products.
3. **Checkout**:
   - Streamlined checkout process for seamless user experience.
4. **Order History**:
   - View past purchases and order details.
5. **Profile Management**:
   - Update and manage user profile settings.



## DevOps Workflow
### Pipeline Stages
1. **Plan**:
   - Frontend mockups and backend architecture diagrams.
   - Tools: Lucidchart was used for visual design.

2. **Develop**:
   - Modular codebase with Django.
   - Styled with Tailwind CSS.
   - Code hosted on GitHub with branching strategies.

3. **Build & Test**:
   - Automated builds and tests triggered on every push.
   - Tools: GitHub Actions for CI, Docker for environment consistency.

4. **Deploy**:
   - Deployment using Dockerized containers.
   - Hosting on Render for production environments.

5. **Monitor & Feedback**:
   - Application monitoring with Prometheus and Grafana.
   - Error tracking integrated with GitHub Issues and Slack.



## Installation & Usage
### Prerequisites
- Python 3.x
- Docker
- Django Framework

### Local Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd e_commerce-master
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000/`.

### Docker Installation
1. Build the Docker image:
   ```bash
   docker build -t e_commerce .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 e_commerce
   ```



## Dockerfile Example
```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

RUN node -v && npm -v

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY theme/static_src/package.json ./theme/static_src/

WORKDIR /app/theme/static_src
RUN npm install -g yarn && yarn install


WORKDIR /app
COPY . .

RUN python manage.py makemigrations
RUN python manage.py makemigrations stores
RUN python manage.py migrate

RUN python manage.py seed_db_api


RUN python manage.py tailwind build

RUN python manage.py collectstatic

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=e_commerce.settings
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "e_commerce.wsgi:application"]
```



## GitHub Actions Workflow Example
**`.github/workflows/ci-cd.yml`**
```yaml
name: Django CI

on:
  push:
    branches: [ "dev" ]
  pull_request:
    branches: [ "dev" ]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      max-parallel: 4
      matrix:
        python-version: [3.8]

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run Tests
      run: |
        python manage.py test
```



## Future Works
1. **Payment Integration**:
   - Add multiple payment gateways for a seamless checkout experience.
2. **Admin Dashboard**:
   - Include analytics and order management tools.
3. **Two-Factor Authentication (2FA)**:
   - Enhance security with additional authentication layers.
4. **FAQs and Support**:
   - Create a user-friendly FAQ section and integrate support options.
5. **Enhanced Monitoring**:
   - Incorporate AI-driven insights for proactive performance monitoring.



## Reflections
### Benefits
- Modular architecture and automated pipelines enable efficient development and deployment.
- Tailwind CSS ensured a responsive and modern UI.
- Dockerized environments provided consistency across development and production.

### Challenges
- Managing the CI/CD pipeline required understanding new tools.
- SQLite is not ideal for large-scale production but sufficed for this phase.

### Lessons Learned
- DevOps practices reduced manual effort and downtime.
- Combining open-source tools requires thoughtful selection for compatibility and scalability.



## References
All references follow the [University of Suffolk Harvard Style](https://libguides.uos.ac.uk/academic/referencing/Harvard).

