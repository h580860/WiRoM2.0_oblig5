# Instructions for the usage of the automatic robot generation script

## Requirements
The script requires python 3 to run, but has no library dependencies. 

## Current functionality
#### Purpose
This purpose of this script is to automate the process of adding a new robot to WiRoM. Instead of having to 
manually add data to certain files, the user should be able to just run a script in the terminal, and the process
should be done automatically.
#### Functionality
The script uses a template for the data, and appends the new data for the new robot to the correct files. Currently, 
the user cannot set most of the parameters, as they are set according to the previously added robots. Examples of 
this is new locations in the world and controller names. The new location for the robot is dependant of the locations 
of the existing robots, as it will be put next to the last robot. The name for the robot will also be dependant of
the existing robots.

## Usage
The script takes in arguments from the user, which is either **generate** or **reset**. 
- **generate** takes in a second argument, which is the type of robot the user wants to add. This can be either
**moose** og **mavic2pro**. 
- **reset** resets the configurations to use the "default" settings, and resets the configuration files back to its
original state.

The script is run as a normal python script, with the arguments coming after the file name  

*Generating a new moose*:  
`python generate_robot.py generate moose`  

*Generate a new Mavic2Pro*:  
`python generate_robot.py generate mavic2pro`

*Reset to default configuration*:  
`python generate_robot.py reset`


## Troubleshooting
This is far from a perfect implementation, and with the nature of creating and deleting files, there comes 
a risk of not everything going as intended every run.  
A common error occurrence is a problem with deleting the controllers when using the `reset` command. Sometimes an 
error is thrown, and the script doesn't successfully delete all the added controllers. A simple solution to this 
problem is to just manually delete the new controller directories if the script fails to delete them.  

The controllers can be found in `/backend/controllers`. As of now, there are a lot of unused controllers there, however the newly 
created ones are easy to spot. The controllers **moose_controller** and **mavic2pro_controller** are
the *default controllers*, and **should not** be deleted. 
On the other hand, the controllers named **moose_controllerx** and **mavic2pro_controllerx**, where 
**x** is a number from 2 and up, are the new controllers. For example, after running the *generate moose* command once,
there will be a new directory in `/backend/controllers` named **moose_controller2**. This directory (and the similarly
created ones) can be deleted safely, if the script fails to do so.  

## Implementation details (technical)
#### Adding a robot to the Webots world
1. Retrieves the robot world data from the robot template file
2. Reads the world map
3. Gets all the robot of given type, and
   1. Get all the translations (their x, y and z locations)
   2. Finds the lowest one, which will depend on the robot type
   3. Creates a new transformation for the new robot, but with an increased/decreased value (depending on the robot type)
4. Adds the new parameters, e.g., robot name and robot controller
5. Appends it to the world file


#### Adding a robot to the config file
*Prerequisite: It needs to have read the translation from the world file first.*
1. Retrieves the robot config data from the robot template file
2. Set its new position, which was retrieved in the previous section from the world file. 
3. Set the new port number
4. Set the new key name, to be used in the json object.
5. Write the changes to the config file. 


#### Adding a robot to the data file
1. Retrieves the robot datafile data from the robot template file
2. Set the port number
3. Set the key name, to be used in the json object
4. Update the "testmission", which is simply a preset mission for the new robots to move forward
5. Write the changes to the data file


#### Adding new controllers for the robot
1. Update new controller names
2. Copy the initial controller of that robot type, with updated names
3. Write to the new controller files
4. Update the routing key lookup table
5. Append the new controller name to the save file


#### Reset to default values
1. Resets the world file, config file and data file to their defaults
2. Deletes the created controller directories.
3. Deletes the save file. 