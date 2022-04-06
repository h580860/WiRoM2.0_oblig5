import fs from 'fs';
// import { CompositeGeneratorNode, NL, processGeneratorNode } from 'langium';
import { CompositeGeneratorNode, processGeneratorNode } from 'langium';
import path from 'path';
import { DslCommand } from '../language-server/generated/ast';
import { extractDestinationAndName } from './cli-util';

export function generateJson(dslCommand: DslCommand, filePath: string, destination: string | undefined): string {
    const data = extractDestinationAndName(filePath, destination);
    // const generatedFilePath = `${path.join(data.destination, data.name)}.js`;
    // const generatedFilePath = `${path.join(data.destination, data.name)}.json`;
    const generatedFilePath = `${path.join(data.destination, dslCommand.robotName.name)}.json`;

    const fileNode = new CompositeGeneratorNode();
    // fileNode.append('"use strict";', NL, NL);
    // model.greetings.forEach(greeting => fileNode.append(`console.log('Hello, ${greeting.person.ref?.name}!');`, NL));

    interface DslRobotData {
        commandType: string;
        robotType: string;
        name: string;
        location: Location
    }

    interface Location {
        x?: number;
        y?: number;
    }


    let currentJsonData: DslRobotData = {
        commandType: dslCommand.commandType.value,
        robotType: dslCommand.robotType.value,
        name: dslCommand.robotName.name,
        location: {
            x: dslCommand.xValue.positionValue,
            y: dslCommand.yValue.positionValue
        }
    }
    fileNode.append(JSON.stringify(currentJsonData));

    if (!fs.existsSync(data.destination)) {
        fs.mkdirSync(data.destination, { recursive: true });
    }
    fs.writeFileSync(generatedFilePath, processGeneratorNode(fileNode));
    return generatedFilePath;
}

export function generateController(dslCommand: DslCommand, filePath: string, destination: string | undefined): string {
    const data = extractDestinationAndName(filePath, destination);
    // const generatedFilePath = `${path.join(data.destination, data.name)}.js`;
    // const generatedFilePath = `${path.join(data.destination, data.name)}.py`;
    const generatedFilePath = `${path.join(data.destination, dslCommand.robotName.name)}.py`;

    const fileNode = new CompositeGeneratorNode();

    fileNode.append(`print(f"Hello '${dslCommand.robotName.name}'!")`)

    if (!fs.existsSync(data.destination)) {
        fs.mkdirSync(data.destination, { recursive: true });
    }
    fs.writeFileSync(generatedFilePath, processGeneratorNode(fileNode));
    return generatedFilePath;
}

