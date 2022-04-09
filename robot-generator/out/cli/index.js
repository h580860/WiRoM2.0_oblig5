"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteNewFiles = exports.generateAction = void 0;
// import colors from 'colors';
const commander_1 = require("commander");
const module_1 = require("../language-server/generated/module");
const robot_generator_module_1 = require("../language-server/robot-generator-module");
const cli_util_1 = require("./cli-util");
const generator_1 = require("./generator");
const deleter_1 = require("./deleter");
const generateAction = (fileName, opts) => __awaiter(void 0, void 0, void 0, function* () {
    const services = (0, robot_generator_module_1.createRobotGeneratorServices)().RobotGenerator;
    const model = yield (0, cli_util_1.extractAstNode)(fileName, services);
    // For each DSL command in the model, generate a JSON file and a controller
    model.dslCommands.forEach(command => {
        const generatedJSONFilePath = (0, generator_1.generateJson)(command, fileName, opts.destination);
        // console.log(colors.green(`JSON file generated successfully: ${generatedJSONFilePath}`));
        console.log(`JSON file generated successfully: ${generatedJSONFilePath}`);
        const generatedControllerFilePath = (0, generator_1.generateController)(command, fileName, opts.destination);
        // console.log(colors.green(`Controller file generated successfully: ${generatedControllerFilePath}`));
        console.log(`Controller file generated successfully: ${generatedControllerFilePath}`);
    });
});
exports.generateAction = generateAction;
const deleteNewFiles = (fileName, opts) => __awaiter(void 0, void 0, void 0, function* () {
    (0, deleter_1.deleteAllNewFilesFromDSL)(fileName, opts.destination);
    console.log(`Finished deleting files`);
});
exports.deleteNewFiles = deleteNewFiles;
function default_1() {
    const program = new commander_1.Command();
    program
        // eslint-disable-next-line @typescript-eslint/no-var-requires
        .version(require('../../package.json').version);
    const fileExtensions = module_1.RobotGeneratorLanguageMetaData.fileExtensions.join(', ');
    program
        .command('generate')
        .argument('<file>', `source file (possible file extensions: ${fileExtensions})`)
        .option('-d, --destination <dir>', 'destination directory of generating')
        // .description('generates JavaScript code that prints "Hello, {name}!" for each greeting in a source file')
        .description('generates a JSON file and a controller for the robot')
        .action(exports.generateAction);
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
        .action(exports.deleteNewFiles);
    program.parse(process.argv);
}
exports.default = default_1;
//# sourceMappingURL=index.js.map