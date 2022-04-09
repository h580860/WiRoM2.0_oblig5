// import colors from 'colors';
import { Command } from 'commander';
import { Model } from '../language-server/generated/ast';
import { RobotGeneratorLanguageMetaData } from '../language-server/generated/module';
import { createRobotGeneratorServices } from '../language-server/robot-generator-module';
import { extractAstNode } from './cli-util';
import { generateJson, generateController } from './generator';
import { deleteAllNewFilesFromDSL } from './deleter';

export const generateAction = async (fileName: string, opts: GenerateOptions): Promise<void> => {
    const services = createRobotGeneratorServices().RobotGenerator;
    const model = await extractAstNode<Model>(fileName, services);

    // For each DSL command in the model, generate a JSON file and a controller
    model.dslCommands.forEach(
        command => {
            const generatedJSONFilePath = generateJson(command, fileName, opts.destination);
            // console.log(colors.green(`JSON file generated successfully: ${generatedJSONFilePath}`));
            console.log(`JSON file generated successfully: ${generatedJSONFilePath}`);
            const generatedControllerFilePath = generateController(command, fileName, opts.destination);
            // console.log(colors.green(`Controller file generated successfully: ${generatedControllerFilePath}`));
            console.log(`Controller file generated successfully: ${generatedControllerFilePath}`);
        }
    )
};

export const deleteNewFiles = async (fileName: string, opts: GenerateOptions): Promise<void> => {
    deleteAllNewFilesFromDSL(fileName, opts.destination);
    console.log(`Finished deleting files`);

}

export type GenerateOptions = {
    destination?: string;
}

export default function (): void {
    const program = new Command();

    program
        // eslint-disable-next-line @typescript-eslint/no-var-requires
        .version(require('../../package.json').version);

    const fileExtensions = RobotGeneratorLanguageMetaData.fileExtensions.join(', ');
    program
        .command('generate')
        .argument('<file>', `source file (possible file extensions: ${fileExtensions})`)
        .option('-d, --destination <dir>', 'destination directory of generating')
        // .description('generates JavaScript code that prints "Hello, {name}!" for each greeting in a source file')
        .description('generates a JSON file and a controller for the robot')
        .action(generateAction);

    // program.parse(process.argv);

    // const programDelete = new Command();
    // programDelete
    //     // eslint-disable-next-line @typescript-eslint/no-var-requires
    //     .version(require('../../package.json').version);

    // programDelete
    //     .command('delete')
    //     .description('delete all of the generated files')
    //     .action(deleteNewFiles);

    // programDelete.parse(process.argv)

    program
        .command('delete')
        .argument('<file>', `source file (possible file extensions: ${fileExtensions})`)
        .option('-d, --destination <dir>', 'destination directory of generating')
        .description('delete all of the generated files from the DSL')
        .action(deleteNewFiles)

    program.parse(process.argv);
}
