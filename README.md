<h2>Architecture</h2>
<img width="1408" height="768" alt="arch" src="https://github.com/user-attachments/assets/f6efeca6-cf1c-4465-bb50-90411740dc06" />

<h2>Project Purpose</h2>
This project aims to build end-to-end data pipeline that extracts an on-premise SQL Server database into a Data Warehouse (Snowflake). 
In this project we are moving the data from local infrastructure to the cloud via batch mode.

<h2>Tech Stack</h2>
<ul>
<li>Source Database: SQL Server (Local)</li>
<li>API Layer: FastAPI, Uvicorn, PyODBC (Dockerized)</li>
<li>Connectivity: Cloudflare Tunnels (Secure local-to-cloud exposure)</li>
<li>Infrastructure as Code: Terraform (Modular AWS provisioning)</li>
<li>Orchestration: AWS Step Functions (State Machine)</li>
<li>Compute & Ingestion: AWS Lambda (Extraction), AWS EMR (Distributed PySpark Transformation)</li>
<li>Storage: AWS S3 (Data Lake)</li>
<li>Monitoring: AWS SNS (Email alerting on failure)</li>
<li>Data Warehouse: Snowflake (External tables over S3)</li>
</ul>

<h2>Key Features</h2>
<ul>
  <li>Containerization: The FastAPI layer is Dockerized, which makes it work on any machine.</li>
  <li>Modular Terraform: Infrastructure is organized into different modules (VPC, IAM, Storage, Compute).</li>
  <li>Resilient Orchestration: AWS Step Functions manage and orchestrate the workflow, with error-handling branches that triggers AWS SNS for email notifications.</li>
  <li>Distributed Processing: Builds star schema model using pyspark scripts via EMR cluster.</li>
</ul>

<h2>Monitoring & Alerts</h2>
The AWS Step Function logic checks if the Lambda or the EMR Spark Job fails:
<ul>
<li> The State Machine transitions to a Fail state.</li>
<li> An SNS Topic is triggered.</li>
<li> An email alert is sent with the error details.</li>
</ul>
<img width="500" height="300" alt="Image" src="https://github.com/user-attachments/assets/7a9ff3d3-7c89-4761-af6f-f4a2d793a671" />
