# Mobility House README

# Quick Start Guide
## Set Up
- Make sure that python3 and rabbitmq are installed
- Create a virtual environment and install the packages
```
python3 -m venv ./
source bin/activate
pip3 install -r requirements.txt
```

If rabbitmq is not running, it may be necessary to start the server:
### Linux
`sudo service rabbitmq-server start`
### MacOS
`rabbitmq-server`

## Run Simulation
This will print the results of the simulation to the `results.txt` file.
`python3 run.py`

## Run Tests
`python3 -m unittest tests/test.py`


# Code Overview
## Meter
For the Meter section, I assumed a 24-hour simulation with samples taken every two seconds. The values were random floats between 0 and 9000 Watts. However, the values only change in periods of time between two seconds and four hours. This allows for a more realistic simulation. For example, perhaps the meter value increases by 200 Watts for three hours - this could be a single appliance being turned on for three hours and then being shut off.

## PV Simulator
For the PV Simulator section, I created a normally distributed graph (source referenced below) to simulate the amount of sunlight that would be processed by the photovoltaic cells throughout the period of a day. The graph peaks at 2 PM with a standard deviation of three hours and a maximum value of 3500 Watts. This ensures that early morning and late night hours will have lower PV values (i.e. approximately 500 Watts at 8 AM and 8 PM) and the middle of the day will have higher PV values (3500 Watts at 2 PM). The variables are defined at the top of the file so that they can be easily changed for a new simulation.

When the values are printed to the `results.txt` file, the "Total Usage" value is the PV value (the number of watts being captured) minus the Meter value (the number of watts being used), and therefore it is often a negative value.


# Obstacles / Lessons Learned
My experience with Docker is pretty limited, as I have used it in projects but I have only joined the projects after Docker was initially set up. I thought that this would be a great opportunity to try to create a Docker container so that it would be a clean working environment and it would be more likely to work on another person's machine. Though I tried to follow a few tutorials online, I wasn't able to get RabbitMQ working with the rest of the code. I suspect that the problem was one (or both) of the following:
- I wasn't accessing the localhost variable and/or exposing the ports correctly inside the container
- I wasn't allowing the RabbitMQ server to start up fully before trying to access it in my code

However, I was able to run my basic code (nothing involving Rabbit) inside the Docker container, so I felt that it was a minor success and I was able to gain some experience with Docker.


# Future Changes
If I had unlimited time, an obvious addition to this project would be to make a frontend. The frontend could include a form where users could put in their own values for all of the variables (i.e. the maximum PV value). Upon submission, the page would update with graphs of the new simulation (probably using a library like D3).

Additionally, it would be an interesting learning experience to successfully get Docker working with the project.


# References
- Equation for Normal Distribution function: http://mathworld.wolfram.com/NormalDistribution.html
- RabbitMQ Tutorials for Python: https://www.rabbitmq.com/tutorials/tutorial-one-python.html
