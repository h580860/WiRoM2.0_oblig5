grammar RobotGenerator

entry Model:
    (dslCommands+=DslCommand)*;


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
