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
   - .gitignore
   - docker-compose.yml
   - Dockerfile
   - env_local.ini
   - requirements.txt
   - README.md

## Assumptions made for this project

1. The JSON structure of messages retrieved from the SQS queue remains consistent.
2. Messages lacking essential field values in their data are not included in the database insertion process.
3. When app_version is a decimal, it is split on . with only the integer part before the . considered as its type, as it is treated as an integer.
4. Masking of device_id and ip utilizes SHA512 and does not require a reversal process.

## Improving the current version

1. While we currently handle basic errors, there's room to implement additional checks to address a broader range of exceptions.
2. At the moment, we process one message at a time, but there's an opportunity to boost performance by implementing batch processing.
3. Consider incorporating a logging mechanism that allows for various log types, such as debug, error, and info, with the flexibility to switch between them.
4. Enhance the test suite by adding more unit tests; presently, the code focuses solely on validating the accuracy of the device_id and ip masking operations.


## Production changes 

1. Leveraging container orchestration solutions like Kubernetes can further enhance our existing Docker setup.
2. Enhance database performance through optimization techniques like indexing and sharding.
3. Implement GitHub Actions for an efficient CI/CD pipeline.
4. Utilize monitoring tools such as Prometheus or Datadog to diagnose issues and detect patterns.
5. Employ logging tools like Logstash to enhance logging capabilities.
6. Scale horizontally by adding multiple nodes with a load balancer and implement auto-scaling based on resource requirements.
7. Utilize a reliable open-source stream processing platform like Apache Kafka.

## About Me
I am Kedar Takwane, a graduate student at the University of Illinois at Urbana-Champaign, pursuing a Master's degree in Computer Science. <br>
Currently, I am engaged as a Research Assistant, where my responsibilities encompass full-stack development and the development of recommendation systems. Prior to this, I have accumulated three years of industry experience as a Software Engineer.

### Contact Information
**Email:** [takwane2@illinois.edu](mailto:takwane2@illinois.edu)
