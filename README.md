# Cloud Computing HW1

### Purpose 
This assignment focus on the process of automating the infrastructure setup and application deployment on AWS. 
The application is very simple and far from being robust.

### Description 
Simple parking management system with 2 HTTP endpoints:
* POST /entry?plate=123-123-123&parkingLot=382 
  * Returns ticket id

* POST /exit?ticketId=1234
  * Returns the license plate, total parked time, the parking lot id and the charge (based on 15 minutes increments).


### Setup on AWS
Use setup.sh to provision an Ubuntu 20.04 ec2 instance (free-tier) and installs the packages and infrastructure required to run the application.
* Redis server
* Python Flask 
* The app code (very basic and simple, no persistency and other real world app)

Before you run this script you need to make sure you have [AWS CLI](https://aws.amazon.com/cli/) installed on your local machine.

