import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { ListGroup, ListGroupItem, ToggleButton, ToggleButtonGroup, ButtonToolbar } from 'react-bootstrap';
import { ReactSortable } from "react-sortablejs";


class Robot extends Component {
  state = {
    list: this.props.state.robots[this.props.state.selectedRobot].simpleactions,
    // commonNames: this.props.state.commonSimpleactionNames,
  }

  componentDidMount() {
    this.removeCommonNameFromList();
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.state.selectedRobot !== "Common") {
      console.log("NOT COMMON")
      this.setState({
        // list: nextProps.state.robots[nextProps.state.selectedRobot].simpleactions.filter(x => x.name !== "go_forward")
        list: nextProps.state.robots[nextProps.state.selectedRobot].simpleactions.filter(x => !nextProps.state.commonSimpleactionNames.has(x.name))
      })
      console.log("filtered: ", nextProps.state.robots[nextProps.state.selectedRobot].simpleactions.filter(x => !nextProps.state.commonSimpleactionNames.has(x.name)))
      // console.log("commonNames in robot.js: ", this.state.commonNames)
      console.log("commonNames in robot.js FROM NEXTPROPS: ", nextProps.state.commonSimpleactionNames);
    }
    else {
      console.log("common")
      this.setState({
        list: nextProps.state.robots[nextProps.state.selectedRobot].simpleactions
      })
    }

    // console.log("componentWill..")
    // this.removeCommonNameFromList();
  }

  removeCommonNameFromList = () => {
    // Remove the elements from the list which already exists in the "Commun" column

    // const newList = this.state.list.filter(simpleaction => !this.state.commonNames.has(simpleaction.name));
    const newList = this.state.list.filter(simpleaction => simpleaction.name !== "go_forward");
    console.log("newList: ", newList);
    this.setState({ list: newList });
  }

  render() {
    return (
      <div>
        <h3>
          Robot simpleactions
        </h3>

        <ButtonToolbar style={{ marginBottom: "15px" }}>
          <ToggleButtonGroup type="radio" name="options">
            {Object.keys(this.props.state.robots).map(robot => (
              <ToggleButton
                size="sm"
                variant={robot === this.props.state.selectedRobot ? "dark" : "outline-dark"}
                onClick={this.props.handleRobotClick(robot)}
              >
                {robot}
              </ToggleButton>))}
          </ToggleButtonGroup>
        </ButtonToolbar>

        <ListGroup style={{ overflow: "scroll" }}>
          {/* <ListGroupItem>
            Language: {this.props.state.robots[this.props.state.selectedRobot].language}
          </ListGroupItem>

          <ListGroupItem>
            Port: {this.props.state.robots[this.props.state.selectedRobot].port}
          </ListGroupItem> */}

          <div style={{ marginBottom: "15px" }}></div>

          <ReactSortable
            list={this.state.list}
            setList={newState => this.setState({ list: newState })}
            sort={false}
            group={{ name: 'shared', pull: 'clone', put: false }}
          >
            {/* <ListGroupItem>Test</ListGroupItem> */}
            {this.state.list.map(sa => // {
              // if (!this.state.commonNames.has(sa.name)) {
              //   return <ListGroupItem>{makeReadable(sa.name)}</ListGroupItem>
              // }
              <ListGroupItem>{makeReadable(sa.name)}</ListGroupItem>
              // }
            )}
          </ReactSortable>
        </ListGroup>
      </div>);
  }
}

function makeReadable(saName) {
  saName = saName.replace(/_/g, " ")
  return saName.charAt(0).toUpperCase() + saName.slice(1)
}


export default Robot