"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateController = exports.generateJson = void 0;
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
    const generatedFilePath = `${path_1.default.join(data.destination, dslCommand.robotName.name)}.py`;
    const fileNode = new langium_1.CompositeGeneratorNode();
    fileNode.append(`print(f"Hello '${dslCommand.robotName.name}'!")`);
    if (!fs_1.default.existsSync(data.destination)) {
        fs_1.default.mkdirSync(data.destination, { recursive: true });
    }
    fs_1.default.writeFileSync(generatedFilePath, (0, langium_1.processGeneratorNode)(fileNode));
    return generatedFilePath;
}
exports.generateController = generateController;
//# sourceMappingURL=generator.js.map