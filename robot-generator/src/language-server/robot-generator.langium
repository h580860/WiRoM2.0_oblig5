grammar RobotGenerator

entry Model:
    (persons+=Person | greetings+=Greeting | dslCommands+=DslCommand)*;

Person:
    'person' name=ID;

Greeting:
    'Hello' person=[Person:ID] '!';

// entry Model:
//     (commands += Command)*;

// RobotType:
// 	MOOSE="moose" |
// 	MAVIC2PRO="mavic2pro" |
// 	OP2="op2" |
// 	BB8="bb8"
// ;

RobotType:
    value = ("moose" | "mavic2pro" | "op2" | "bb8" | "pr2")
;

PositionValue:
	positionValue = INT
;

RobotName:
	name = STRING
;

CommandType:
	// {AddRobot} value="addRobot" |
	// {RemoveRobot} value="removeRobot"
    // addRobot = "addRobot" |
	// removeRobot ="removeRobot"
    value = ("addRobot" | "removeRobot")
;

DslCommand:
	commandType=CommandType '(' robotType=RobotType ',' robotName=RobotName? ',' xValue=PositionValue? ',' yValue=PositionValue? ')' ';'
;


hidden terminal WS: /\s+/;
terminal ID: /[_a-zA-Z][\w_]*/;
terminal INT returns number: /[0-9]+/;
terminal STRING: /"[^"]*"|'[^']*'/;

hidden terminal ML_COMMENT: /\/\*[\s\S]*?\*\//;
hidden terminal SL_COMMENT: /\/\/[^\n\r]*/;
