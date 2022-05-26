"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.appendToNewRobotsFile = exports.generateController = exports.generateJson = void 0;
const fs_1 = __importDefault(require("fs"));
// import { CompositeGeneratorNode, NL, processGeneratorNode } from 'langium';
const langium_1 = require("langium");
const path_1 = __importDefault(require("path"));
const cli_util_1 = require("./cli-util");
function generateJson(dslCommand, filePath, destination) {
    const data = (0, cli_util_1.extractDestinationAndName)(filePath, destination);
    // const generatedFilePath = `${path.join(data.destination, data.name)}.js`;
    // const generatedFilePath = `${path.join(data.destination, data.name)}.json`;
    const generatedFilePath = `${path_1.default.join(data.destination, dslCommand.robotName.name)}.json`;
    const fileNode = new langium_1.CompositeGeneratorNode();
    let currentJsonData = {
        commandType: dslCommand.commandType.value,
        robotType: dslCommand.robotType.value,
        name: dslCommand.robotName.name,
        location: {
            x: dslCommand.xValue.positionValue,
            y: dslCommand.yValue.positionValue
        }
    };
    fileNode.append(JSON.stringify(currentJsonData));
    if (!fs_1.default.existsSync(data.destination)) {
        fs_1.default.mkdirSync(data.destination, { recursive: true });
    }
    fs_1.default.writeFileSync(generatedFilePath, (0, langium_1.processGeneratorNode)(fileNode));
    return generatedFilePath;
}
exports.generateJson = generateJson;
function generateController(dslCommand, filePath, destination) {
    const data = (0, cli_util_1.extractDestinationAndName)(filePath, destination);
    // const generatedFilePath = `${path.join(data.destination, data.name)}.js`;
    // const generatedFilePath = `${path.join(data.destination, data.name)}.py`;
    const generatedFilePath = `${path_1.default.join(data.destination, `${dslCommand.robotName.name}_controller`)}.py`;
    const fileNode = new langium_1.CompositeGeneratorNode();
    // extract the variables we need
    const robotType = dslCommand.robotType.value;
    const robotTypeCapitalized = capitalizeType(robotType);
    const robotName = dslCommand.robotName.name;
    // TODO length of this line in the editor
    const controllerTemplate = `import sys\nimport os\n\ncontroller_path = os.path.join(os.getcwd(), os.pardir)\nsys.path.insert(0, controller_path)\n\nfrom ${robotType}_controller_class import ${robotTypeCapitalized}ControllerClass\n${robotType}_controller = ${robotTypeCapitalized}ControllerClass(\"${robotName}\")\n${robotType}_controller.initiate_threads()`;
    // fileNode.append(`print(f"Hello '${dslCommand.robotName.name}'!")`)
    fileNode.append(controllerTemplate);
    if (!fs_1.default.existsSync(data.destination)) {
        fs_1.default.mkdirSync(data.destination, { recursive: true });
    }
    fs_1.default.writeFileSync(generatedFilePath, (0, langium_1.processGeneratorNode)(fileNode));
    return generatedFilePath;
}
exports.generateController = generateController;
function appendToNewRobotsFile(dslCommand, filePath, destination) {
    const data = (0, cli_util_1.extractDestinationAndName)(filePath, destination);
    const newRobotsListFilePath = `${path_1.default.join(data.destination, "newRobots")}.txt`;
    const fileNode = new langium_1.CompositeGeneratorNode();
    const robotName = dslCommand.robotName.name;
    fileNode.append(robotName + '\n');
    if (!fs_1.default.existsSync(newRobotsListFilePath)) {
        fs_1.default.writeFileSync(newRobotsListFilePath, (0, langium_1.processGeneratorNode)(fileNode));
    }
    else {
        fs_1.default.appendFileSync(newRobotsListFilePath, (0, langium_1.processGeneratorNode)(fileNode));
    }
}
exports.appendToNewRobotsFile = appendToNewRobotsFile;
function capitalizeType(robotType) {
    return robotType.charAt(0).toUpperCase() + robotType.slice(1);
}
//# sourceMappingURL=generator.js.map