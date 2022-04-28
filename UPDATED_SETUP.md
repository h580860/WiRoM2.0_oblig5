# Wirom2.0 Setup Manual

This is the temporary setup manual for Wirom2.0

## Required installations

### Webots
Install this version of Webots: https://github.com/cyberbotics/webots/releases/tag/R2021b

### Python:
Download Python 3.9 from their website: 
https://www.python.org/downloads/release/python-3912/ 
#### Note:
We are using this version because Webots only supports up to Python 3.9. Even though the controllers are not implemented through the editor in Webots, it’s best to use the same version to make sure that they are compatible. 


### Node.js / npm:
Downloaded from: https://nodejs.org/en/ 

### RabbitMQ:
Choose the correct operating system from: 
https://www.rabbitmq.com/download.html \
With MacOS it is recommended to use the *Homebrew* package installer.\
On Windows it is recommended to either use the *Chocolatey* package manager or use the installer as an administrative user. 

### Command Line Interface: 
To follow along the next steps, you need to use command line interface. \
On Windows, I have mainly been using the Windows Terminal: \
https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701?hl=en-us&gl=US \
MacOS users can use the Terminal command line. 

### Cloning the repository
To download the source code, clone the repository to your machine using the command: 
```
git clone https://github.com/gunnarkleiven/WiRoM2.0.git
```
To run the system, you need to run 3 processes:
-	The web interface
-	The backend Server
-	Webots simulator

## Running the web interface 
Navigate to the *web_interface* folder:
```
cd Wirom2.0/web_interface
```
Before running it for the first time, you need to install the required packages by running the command
```
npm install
```
After this, start the web interface by running
```
npm start
```

## Running the flask (Python) server
Navigate to the proper folder by the command
```
cd Wirom2.0/backend
```
To help manage the different dependencies, it is useful to create a Python virtual environment. When you install it for the first time, run the following command on **Windows**
```
python -m venv .venv
```
or on **macOS/Linux**:
```
python3 -m venv .venv

```
The last argument is the name of the directory of the environment, in this case *".venv"* \
\
To initiate the virtual environment, run the command \
On **Windows**
```
./.venv/Scripts/activate
```
on **Mac**
```
source .venv/bin/activate
```

After this, you need to install the dependencies. This is done with the command
```
pip install -r requirements.txt
```

Next step is to set the Flask environment variable, using the command
On **Windows**
```
$env:FLASK_APP = "backend"
```
On **MacOS**
```
export FLASK_APP=backend
```
Finally, navigate one folder up
```
cd ..
```
And then start the server
```
flask run
```



