When installing WiRoM2.0, Raquel’s video of installing the program(s) was pretty helpful. Though, doing pretty much the same as described in the WiRoM repo, some changes had to be made. 
Before starting the interface, I had to input this: $env:NODE_OPTIONS = "--openssl-legacy-provider"
After this, you can run “npm start”. 

To start the flask server, the flask_app had to be added to systempath, however that was not enough; so I had to write a different variant in order to have it run: flask --app backend run

For some reason, rabbitmq server hadn’t started on its own, so that has to be manually started. This can be done by looking up “RabbitMQ Service – start” on your local machine, and run it.  
