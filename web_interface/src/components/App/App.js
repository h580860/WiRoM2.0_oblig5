import React, { Component } from 'react';
import data from '../../data';
import Simpleaction from '../Simpleaction/Simpleaction'
import Mission from '../Mission/Mission'
import Task from '../Task/Task'
import Robot from '../Robot/Robot'
import NewMission from '../NewMission/NewMission'
import NewTask from '../NewTask/NewTask'
import MissionTimeline from '../MissionTimeline/MissionTimeline'
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'
import { Button, Form, Dropdown, Container, Col, Row, Toast, ListGroup } from 'react-bootstrap';
import Editor from "@monaco-editor/react";
import algorithmEditorTemplateFile from '../EditorTemplates/algorithmEditorTemplate.txt';

//Toggle used by the Dropdown component when searching for simpleactions
const CustomToggle = React.forwardRef(({ children, onClick }, ref) => (
  <a
    href=""
    ref={ref}
    onClick={e => {
      e.preventDefault();
      onClick(e);
    }}
  >
    {children}
    &#x25bc;
  </a>
));

//Menu used by the Dropdown component when searching for simpleactions
const CustomMenu = React.forwardRef(
  ({ children, style, className, 'aria-labelledby': labeledBy }, ref) => {
    const [value, setValue] = React.useState('');

    return (
      <div
        ref={ref}
        style={style}
        className={className}
        aria-labelledby={labeledBy}
      >
        <Form.Control
          autoFocus
          className="mx-3 my-2 w-auto"
          placeholder="Type to filter..."
          onChange={e => setValue(e.target.value)}
          value={value}
        />
        <ul className="list-unstyled">
          {React.Children.toArray(children).filter(
            child =>
              !value || child.props.children[1].toLowerCase().includes(value) || child.props.children[3].toLowerCase().includes(value),
          )}
        </ul>
      </div>
    );
  },
);

//App class holds the parent state of the system, child-components this state and update it via the functions in this class
class App extends Component {
  state = {
    robots: data.robots,
    selectedRobot: data.defaultSelectedRobot,
    selectedMission: data.defaultSelectedMission,
    selectedTask: data.defaultSelectedTask,
    availableSimpleactions: [],
    missions: data.missions,
    currentMission: data.defaultCurrentMission,
    graphData: { nodes: [{ id: "robot" }], links: [] },
    showTimeline: false,
    showEditor: false,  // The DSL editor
    editorContent: "",
    showEditorToast: false,
    editorToastBody: [],
    showAlgorithmEditor: false,    // Editor for adding new task allocation algorithm
    addedTaskAllocationAlgorithms: ["random_allocation"],
    algorithmEditorContent: "",
    algorithmEditorTemplate: "",
    algorithmEditorFormValue: "",
  }

  componentDidMount() {
    this.handleMissionChange()
    this.handleAvailableSimpleactionsChange()
    // Read the template for the default value of the algorithm editor
    this.readTemplate(algorithmEditorTemplateFile);
    this.setState({ algorithmEditorContent: this.state.algorithmEditorTemplate })
  }

  readTemplate = (filename) => {
    fetch(filename)
      .then(r => r.text()
        .then(text => {
          console.log("Text from template: ", text)
          this.setState({ algorithmEditorTemplate: text });
        })
      );
  }

  //Create new current mission, called everytime the missions changes in the ui
  handleMissionChange = event => {
    let tasks = this.state.missions[this.state.selectedMission].tasks
    let robots = this.state.robots
    let newMission = {}

    //Loop through all simpleactions and add them in order to each robot
    tasks.forEach(task => {
      let robot = task.robot
      if (robot !== "--") {
        task.simpleactions.forEach(simpleaction => {
          console.log(robot)
          let newSimpleactions = []

          if (robot in newMission) {
            newSimpleactions = newMission[robot].simpleactions
            simpleaction.id = newSimpleactions.length
          }

          else {
            newMission[robot] = { port: robots[robot]["port"], language: robots[robot]["language"] }
            simpleaction.id = 0
          }

          newSimpleactions.push(simpleaction)
          newMission[robot].simpleactions = newSimpleactions
        })
      }
    })
    this.setState({ currentMission: newMission })
    console.log(this.state)
  }

  //Create a list of all avaiable simpleactions from the different robots, used for conveniance
  handleAvailableSimpleactionsChange = event => {
    let availableSimpleactions = []

    for (let robot in this.state.robots) {
      this.state.robots[robot].simpleactions.forEach(sa => {
        sa.robot = robot
        availableSimpleactions.push(sa)
      })
    }
    this.setState({ availableSimpleactions: availableSimpleactions })
  }

  //Handle when user clicks a mission to show to the user
  handleMissionClick = missionName => event => {
    let newSelectedTask = ""
    if (this.state.missions[missionName].tasks.length > 0)
      newSelectedTask = this.state.missions[missionName].tasks[0].name

    this.setState({ selectedMission: missionName })
    this.setState({ selectedTask: newSelectedTask })
    this.handleMissionChange()
  }

  //Handle when user clicks a robot to show to the user
  handleRobotClick = name => event => {
    this.setState({ selectedRobot: name });
  }

  //Handle when user clicks a task to show to the user
  handleTaskClick = name => event => {
    this.setState({ selectedTask: name })
  }

  //Handle state for when the user changes arguments for a simpleaction
  handleSimpleactionArgsChange = sa => event => {
    let tasks = this.state.missions[this.state.selectedMission].tasks
    let newSa = sa
    tasks.forEach(task => {
      task.simpleactions.forEach(simpleaction => {
        if (simpleaction === sa) {
          newSa = simpleaction
          newSa.args = event.target.value
        }
      })
    })
    this.setState({ sa: newSa })
    this.handleMissionChange()
  }

  //Handle state for when user changes robot for a simpleaction
  handleTaskAllocationChange = task => event => {
    let tasks = this.state.missions[this.state.selectedMission].tasks
    let newTask = {}
    tasks.forEach(t => {
      if (task === t) {
        newTask = t
        newTask.robot = event.target.value
      }
    })
    this.setState({ task: newTask })
    this.handleMissionChange()
  }

  handleAddNewTask = taskName => event => {
    let mission = this.state.missions[this.state.selectedMission]
    mission.tasks.push({ "name": taskName, "id": mission.tasks.length, simpleactions: [], robot: "--" })
    this.setState({ selectedTask: taskName })
    this.setState({ mission: mission })

    event.preventDefault()
    event.target.reset()
    this.handleMissionChange()
  }

  handleAddNewSimpleaction = sa => event => {
    let tasks = this.state.missions[this.state.selectedMission].tasks
    tasks.forEach(task => {
      if (task.name === this.state.selectedTask)
        task.simpleactions.push({ "name": sa.name, "args": "" })
      tasks[tasks.indexOf(task)] = task
    })
    this.setState({ tasks: tasks })
    this.handleMissionChange()
  }

  handleAddNewMission = missionName => event => {
    let missions = this.state.missions
    missions[missionName] = { "tasks": [] }
    this.setState({ missions: missions })
    this.setState({ selectedMission: missionName })
    this.setState({ selectedTask: "" })

    event.preventDefault()
    event.target.reset();
    this.handleMissionChange()
  }

  handleRemoveTask = task => event => {
    let mission = this.state.missions[this.state.selectedMission]
    mission.tasks.splice(mission.tasks.indexOf(task), 1)
    this.setState({ mission: mission })
    this.handleMissionChange()
  }

  handleRemoveSimpleaction = simpleaction => event => {
    let tasks = this.state.missions[this.state.selectedMission].tasks
    tasks.forEach(task => {
      if (task.name === this.state.selectedTask) {
        task.simpleactions.splice(task.simpleactions.indexOf(simpleaction), 1)
      }
    })
    this.setState({ tasks: tasks })
    this.handleMissionChange()
  }

  //Sortable "drag-and-drop" handling used by ReactSortable in simpleaction component
  handleSimpleactionSortable = newState => {
    let tasks = this.state.missions[this.state.selectedMission].tasks

    tasks.forEach(task => {
      if (task.name === this.state.selectedTask) {
        if (newState > task.simpleactions) {
          newState.forEach(sa => {
            if (!task.simpleactions.includes(sa)) {
              newState[newState.indexOf(sa)] = { "name": sa.name, "args": "", "id": (newState.length - 1) }
            }
          })
        }
        task.simpleactions = newState
      }
    })
    this.handleMissionChange()
    this.setState({ tasks: tasks })
  }

  //Sortable "drag-and-drop" handling used by ReactSortable in simpleaction component
  handleTaskSortable = newState => {
    let missions = this.state.missions
    missions[this.state.selectedMission].tasks = newState
    missions[this.state.selectedMission].tasks.forEach(task => {
      task.id = missions[this.state.selectedMission].tasks.indexOf(task)
    })
    this.handleMissionChange()
    this.setState({ missions: missions })
  }

  //Submit the mission, validate its arguments and send it to the backend
  handleSubmitMission = event => {
    if (validateMission(this.state)) {
      sendMission(this.state);
      event.preventDefault();
    }
    else
      alert('Mission is not valid')
  }

  //Send the mission to the backend to perform automatic task allocation
  //The new task allocation is returned in the response of the request and updated here
  handleSubmitTaskAllocation = event => {
    let response = sendTaskAllocation(this.state);
    response
      .then(res => {
        if (res === undefined)
          throw 'Could not connect to server'
        console.log("Received res = ", res)
        let missions = this.state.missions
        missions[this.state.selectedMission].tasks = res
        console.log(res)
        this.setState({ missions: missions })
        this.handleMissionChange();
      })
      .catch(console.log)

    event.preventDefault();
  }

  handleCBAATaskAllocation = event => {
    console.log("Clicked handleCBAATaskAllocation")
    let response = sendCBAAInitiation(this.state);
    response
      .then(res => {
        if (res === undefined)
          throw 'Could not connect to server'
        console.log("Received CBAA res = ", res)
        let missions = this.state.missions
        missions[this.state.selectedMission].tasks = res
        console.log(res)
        this.setState({ missions: missions })
        this.handleMissionChange();
      })
      .catch(console.log)

    event.preventDefault();
  }

  handleEditorClick = event => {
    // let response = sendDslEditorContent(this.state)
    this.setState({ showEditor: !this.state.showEditor })

  }

  handleEditorChange = (value, event) => {
    this.setState({ editorContent: value })
  }
  handleAlgorithmEditorChange = (value, event) => {
    this.setState({ algorithmEditorContent: value })
  }

  handleSendEditorContentClick = event => {
    let response = sendDslEditorContent(this.state);
    response
      .then(res => {
        console.log(res.output);
        this.toggleShowEditorToast();
        this.setState({ editorToastBody: res.output });
      })
    // TODO stopped here, perhaps implement it the same way as handleSubmitTaskAllocaiton()?
  }

  handleSendAlgorithmEditorContentClick = event => {
    let response = sendAlgorithmEditorContent(this.state)
    response
      .then(res => {
        console.log(`res.name=${res.name}`)
        let new_list = this.state.addedTaskAllocationAlgorithms
        new_list.push(res.name)
        this.setState({ addedTaskAllocationAlgorithms: new_list })
      })
  }

  handleDeleteGeneratedRobots = event => {
    let response = deleteGeneratedRobots()
    response
      .then(res => {
        console.log(res.output);
        this.toggleShowEditorToast();
        this.setState({ editorToastBody: res.output });
      })
  }

  toggleShowEditorToast = () => {
    this.setState({ showEditorToast: !this.state.showEditorToast });
  }

  toggleShowAlgorithmEditor = () => {
    console.log(this.state.algorithmEditorTemplate)
    this.setState({ showAlgorithmEditor: !this.state.showAlgorithmEditor });
  }

  handleEditorFormChange = event => {
    this.setState({ algorithmEditorFormValue: event.target.value })
  }


  handleExecuteNewAlgorithm = (val, event) => {
    console.log(`Wants to execute ${val}`)
    // TODO got here  ons.20 april 17.06. The problem is the undefined event here
    // console.log("Event: ", event);
    let response = executeNewAlgorithm(val, this.state);
    response
      .then(res => {
        if (res === undefined)
          throw 'Could not connect to server'
        let missions = this.state.missions
        missions[this.state.selectedMission].tasks = res
        console.log(res)
        this.setState({ missions: missions })
        this.handleMissionChange();
      })
      .catch(console.log)

    event.preventDefault();
  }

  //render function for the app, upper layer which ties together all components
  render() {
    return (
      <Container fluid>
        <Row style={{ marginTop: "30px" }}>
          <Col xs="9">
            <div className="shadow p-3 mb-5 rounded" style={{ backgroundColor: "#f2f2f2" }}>
              <div className="shadow p-3 mb-5 bg-white rounded">
                <Row>
                  <Mission
                    state={this.state}
                    handleMissionClick={(mission) => this.handleMissionClick(mission)}
                  >
                  </Mission>

                  <NewMission
                    state={this.state}
                    handleAddNewMission={(missionName) => this.handleAddNewMission(missionName)}
                  >
                  </NewMission>

                </Row>
              </div>

              <Row>
                <Col xs={6}>
                  <div className="shadow p-3 mb-5 bg-white rounded">
                    <Task
                      state={this.state}
                      handleTaskClick={(currentMission) => this.handleTaskClick(currentMission)}
                      handleRemoveTask={(task) => this.handleRemoveTask(task)}
                      handleTaskSortable={(newState) => this.handleTaskSortable(newState)}
                      handleTaskAllocationChange={(task) => this.handleTaskAllocationChange(task)}>
                    </Task>

                    <NewTask state={this.state} handleAddNewTask={(taskName) => this.handleAddNewTask(taskName)} print={() => this.print()}>
                    </NewTask>
                  </div>
                </Col>

                <Col xs={6}>
                  {
                    this.state.selectedTask === "" ? <div></div> :
                      <div className="shadow p-3 mb-5 bg-white rounded">
                        <Simpleaction
                          state={this.state}
                          handleSimpleactionArgsChange={(sa) => this.handleSimpleactionArgsChange(sa)}
                          handleSimpleactionRobotChange={(sa) => this.handleSimpleactionRobotChange(sa)}
                          handleRemoveSimpleaction={(sa) => this.handleRemoveSimpleaction(sa)}
                          handleSimpleactionSortable={(newState) => this.handleSimpleactionSortable(newState)}
                        >
                        </Simpleaction>

                        <Dropdown>
                          <Dropdown.Toggle id="dropdown-custom-components" as={CustomToggle} title="Search for simpleaction">
                            Search for simpleaction
                          </Dropdown.Toggle>

                          <Dropdown.Menu as={CustomMenu}>
                            {this.state.availableSimpleactions.map(sa => <Dropdown.Item onClick={this.handleAddNewSimpleaction(sa)}> {sa.name} ({sa.robot}) </Dropdown.Item>)}
                          </Dropdown.Menu>
                        </Dropdown>
                      </div>
                  }
                </Col>

              </Row>

              <Row >
                <Col>
                  <MissionTimeline state={this.state}></MissionTimeline>

                  <Button type="submit" variant="outline-dark" onClick={this.handleSubmitMission}>
                    Send mission
                  </Button>

                  <Button type="submit" variant="outline-dark" onClick={this.handleSubmitTaskAllocation}>
                    Automatic task allocation
                  </Button>
                  <Button type="submit" variant="outline-dark" onClick={this.handleCBAATaskAllocation}>
                    CBAA
                  </Button>
                  {this.state.addedTaskAllocationAlgorithms.map((elem, idx) => (
                    <Button type="submit" variant="outline-dark" key={idx} onClick={(event) => this.handleExecuteNewAlgorithm(elem, event)}>
                      {elem}
                    </Button>
                  ))}
                </Col>
              </Row>
              <Row>
                <Col>
                  <Button style={{ marginTop: "10px" }} type="submit" variant="outline-dark" onClick={this.toggleShowAlgorithmEditor}>
                    {!this.state.showAlgorithmEditor ? "Show Algorithm Editor" : "Hide Algorithm Editor"}
                  </Button>
                </Col>
              </Row>
            </div>
            {this.state.showAlgorithmEditor && <div className="shadow p-3 mb-5 rounded" style={{ backgroundColor: "#f2f2f2" }}>
              <div className="shadow p-3 mb-5 bg-white rounded">
                Editor for creating adding a custom task allocation algorithm
                <Form>
                  <Form.Group className="mb-3" controlId="formFileName">
                    <Form.Label>Algorithm Name</Form.Label>
                    <Form.Control placeholder='Enter the algorithm name' onChange={this.handleEditorFormChange} />
                  </Form.Group>
                </Form>
                <Editor
                  height="20vh"
                  defaultLanguage="python"
                  //defaultValue="# some comment"
                  defaultValue={this.state.algorithmEditorTemplate}
                  onChange={this.handleAlgorithmEditorChange}
                />
                <Button type="submit" variant="outline-dark" onClick={this.handleSendAlgorithmEditorContentClick}>
                  Send new task allocation
                </Button>
              </div>

            </div>
            }
            <div className="shadow p-3 mb-5 rounded" style={{ backgroundColor: "#f2f2f2" }}>
              <div className="shadow p-3 mb-5 bg-white rounded">
                <Button type="submit" variant="outline-dark" onClick={this.handleEditorClick}>
                  {!this.state.showEditor ? "Show Editor" : "Hide Editor"}
                </Button>
                {this.state.showEditor && <div>
                  Editor for using the Robot-Generator DSL
                  <Editor
                    height="20vh"
                    // defaultLanguage="javascript"
                    // defaultValue="// some comment"
                    onChange={this.handleEditorChange}
                  />
                  <Button type="submit" variant="outline-dark" onClick={this.handleSendEditorContentClick}>
                    Send
                  </Button>
                  <Button type="submit" variant="outline-dark" onClick={this.handleDeleteGeneratedRobots}>
                    Delete generated robots
                  </Button>
                </div>}
                {/* <div style={{ minWidth: '300px' }}> */}
                <Toast show={this.state.showEditorToast} onClose={this.toggleShowEditorToast}>
                  <Toast.Header>
                    <strong className="me-auto">Message(s) from the server:</strong>
                  </Toast.Header>
                  <Toast.Body>
                    <ListGroup variant="flush">
                      {this.state.editorToastBody.map((elem, idx) =>
                        <ListGroup.Item>{elem}</ListGroup.Item>
                      )}
                    </ListGroup>
                    {/* {this.state.editorToastBody.forEach(line => (
                      console.log(line)
                    ))} */}
                  </Toast.Body>
                </Toast>
                {/* </div> */}
              </div>
            </div>
          </Col>

          <Col xs={3}>
            <div className="shadow p-3 mb-5 bg-white rounded">
              <Robot
                state={this.state}
                handleRobotClick={(name) => this.handleRobotClick(name)}>
              </Robot>

            </div>
          </Col>
        </Row>
      </Container >
    );
  }
}

//function to validate if simpleactions contain arguments
function validateMission(state) {
  let mission = state.currentMission
  let robots = state.robots
  let isValid = true

  for (let robot in mission) {
    mission[robot].simpleactions.forEach(simpleaction => {
      robots[robot].simpleactions.forEach(sa => {
        if (sa.name === simpleaction.name) {
          if (sa.numArgs !== 0 && simpleaction.args.length === 0)
            isValid = false
        }
      })
    })
  }
  return isValid
}

function sendTaskAllocation(state) {
  console.log('Sending request')
  console.log(JSON.stringify(state.missions[state.selectedMission].tasks))
  console.log(state.missions[state.selectedMission].tasks)
  let res = fetch('http://localhost:5000/allocate', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(state.missions[state.selectedMission].tasks)
  })
    .then(res => { return res.json() })
    .catch(console.log)
  return res
}

function sendCBAAInitiation(state) {
  console.log('Sending request to CBAA task allocation')
  let res = fetch('http://localhost:5000/cbaa_initiation', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(state.missions[state.selectedMission].tasks)
  })
    .then(res => { return res.json() })
    .catch(console.log)
  return res
}

function sendMission(state) {
  console.log('Sending request')
  console.log(state.currentMission);
  fetch('http://localhost:5000/mission', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(state.currentMission)
  })
    .then(res => console.log(res))
    .catch(console.log)
}

function sendDslEditorContent(state) {
  // let testData = { content: "addRobot(moose, \"Stig\", 3, 4);" }
  let res = fetch('http://localhost:5000/robot-generator', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ content: state.editorContent })
  })
    .then(res => {
      console.log(res);
      return res.json();
    })
    .catch(err => {
      console.log(err);
    })
  return res
}

function sendAlgorithmEditorContent(state) {
  console.log('Sending algorithm editor content:\n', state.algorithmEditorContent);
  // let testData = { content: "addRobot(moose, \"Stig\", 3, 4);" }
  let res = fetch('http://localhost:5000/new-algorithm', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(
      {
        algorithm_name: state.algorithmEditorFormValue,
        content: state.algorithmEditorContent,
      })
  })
    .then(res => {
      return res.json();
    })
    .catch(err => {
      console.log(err);
    })
  return res
}

function deleteGeneratedRobots() {
  console.log("Deleting generated robots");
  let res = fetch('http://localhost:5000/deleteGeneratedDSL', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
    .then(res => { return res.json() })
    .catch(console.log)
  return res
}

function executeNewAlgorithm(algorithmName, state) {
  console.log(`executing function ${algorithmName}`);
  console.log("tasks:");
  console.log(state.missions[state.selectedMission].tasks);
  let res = fetch('http://localhost:5000/execute-algorithm', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(
      {
        name: algorithmName,
        tasks: state.missions[state.selectedMission].tasks,
      }),
  })
    .then(res => { return res.json() })
    .catch(console.log)
  return res
}

export default App;
