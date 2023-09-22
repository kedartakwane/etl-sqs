# Creating ETL off a SQS Queue

## Setting up the Project

### Requirements for running
- Docker and docker-compose

`Note`: Other requirements are fetched by docker via docker-compose.

### Setting Up

1. Clone the repository.
2. Run docker-compose file using:

       docker-compose -f docker-compose.yml up -d --build
   
4. Testing local access as mentioned in the document:
   1. Read message from the queue using the command:

           awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue

   2. Check if your table is created in PostgreSQL using the two commands shown below: 

          psql -d postgres -U postgres -p 5432 -h localhost -W
          SELECT * FROM user_logins;

5. To stop the container use:

        docker-compose -f docker-compose.yml down
   

## Test the System

Run unit tests with:
```
pytest tests/.
```
**Note: This is run by default when docker container starts**

## Project Structure
- etl-sqs/
  - src/
    - helpers
      - logins.py
      - queue_service.py
    - run.py
   - tests/
     - test_all.py
   - docker-compose.yml
   - Dockerfile
   - env_local.ini
   - requirements.txt
   - README.md

## Assumptions made for this project

1. The JSON structure for a message fetched from the SQS queue is consistent.
2. Messages lacking the necessary field values in their data are excluded from the database insertion process.
3. If `app_version` is a decimal, then it is split on `.` and only the **integer before the `.` is considered** as the type of this is integer.
4. Masking the `device_id` and `ip` doesn't need to be reversed. Thus, using SHA512.

## Improving the current version

1. Basic errors are handled but more checks can be added to handle any kind of exception.
2. Current one message is processed at a time. Performance can be increased using batch processing.
3. Add a way to log information and give a way to switch between different types of logs like `debug`, `error` and `info`.
4. Adding more unit tests, as the code only checks if the masking done on `device_id` and `ip` is correct.


## Production changes 

1. We have already used docker so using container orchestration like Kubernetes will help.
2. Optimize the database using techniques like indexing and sharding.
3. Using GitHub actions for CI/CD pipeline.
4. Monitoring tools for diagnosing issues and identifying patterns Prometheus or Datadog.
5. Use logging tools like Logstash.
6. Adding multiple nodes with load balancer for horizontal scaling and auto-scale based on the resource requirements.
7. Use open-source, robust stream processing platform like Apache Kafka.

## About Me
I am Kedar Takwane, a graduate student at the University of Illinois at Urbana-Champaign, pursuing a Master's degree in Computer Science. <br>
Currently, I am engaged as a Research Assistant, where my responsibilities encompass full-stack development and the development of recommendation systems. Prior to this, I have accumulated three years of industry experience as a Software Engineer.

### Contact Information
**Email:** [takwane2@illinois.edu](mailto:takwane2@illinois.edu)
