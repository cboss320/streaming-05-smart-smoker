# streaming-05-smart-smoker

# Courtney Pigford 9-21-2023

## Smart Smoker System

Read about the Smart Smoker system here: Smart Smoker
We read one value every half minute. (sleep_secs = 30)
smoker-temps.csv has 4 columns:

[0] Time = Date-time stamp for the sensor reading
[1] Channel1 = Smoker Temp --> send to message queue "01-smoker"
[2] Channe2 = Food A Temp --> send to message queue "02-food-A"
[3] Channe3 = Food B Temp --> send to message queue "02-food-B"
We want know if:

The smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert!)
Any food temperature changes less than 1 degree F in 10 minutes (food stall!)

### Time Windows

Smoker time window is 2.5 minutes
Food time window is 10 minutes
Deque Max Length

At one reading every 1/2 minute, the smoker deque max length is 5 (2.5 min *1 reading/0.5 min)
At one reading every 1/2 minute, the food deque max length is 20 (10 min* 1 reading/0.5 min)
Condition To monitor

If smoker temp decreases by 15 F or more in 2.5 min (or 5 readings)  --> smoker alert!
If food temp change in temp is 1 F or less in 10 min (or 20 readings)  --> food stall alert!
Requirements

#### RabbitMQ server running

pika installed in your active environment
RabbitMQ Admin

See <http://localhost:15672/> Links to an external site.
General Design

How many producer processes do you need to read the temperatures: One producer, built last project.
How many listening queues do we use: three queues, named as listed above.
How many listening callback functions do we need (Hint: one per queue): Three callback functions are needed.

##### Requirements

In your callback function, make sure you generate alerts - there will be a smoker alert and both Food A and Food B will stall.

Your README.md screenshots must show 4 concurrent processes:

Producer (getting the temperature readings)
Smoker monitor
Food A monitor
Food B monitor
In addition, you must show at least 3 significant events.

Run each terminal long enough that you can show the significant events in your screenshots:

Visible Smoker Alert with timestamp
Visible Food A stall with timestamp
Visible Food B stall with timestamp
