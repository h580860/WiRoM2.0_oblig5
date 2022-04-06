"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteAllNewFilesFromDSL = void 0;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const colors_1 = __importDefault(require("colors"));
// // import { CompositeGeneratorNode, NL, processGeneratorNode } from 'langium';
// import { CompositeGeneratorNode, processGeneratorNode } from 'langium';
// import path from 'path';
// import { DslCommand } from '../language-server/generated/ast';
const cli_util_1 = require("./cli-util");
function deleteAllNewFilesFromDSL(filePath, destination) {
    const data = (0, cli_util_1.extractDestinationAndName)(filePath, destination);
    // console.log(`Destination: ${data.destination}, name: ${data.name}`);
    if (fs_1.default.existsSync(data.destination)) {
        // Source: https://stackoverflow.com/questions/27072866/how-to-remove-all-files-from-directory-without-removing-directory-in-node-js
        fs_1.default.readdir(data.destination, (err, files) => {
            if (err)
                throw err;
            for (const file of files) {
                fs_1.default.unlink(path_1.default.join(data.destination, file), err => {
                    if (err)
                        throw err;
                });
            }
        });
    }
    console.log(colors_1.default.green(`Finished deleting files in ${data.destination}`));
}
exports.deleteAllNewFilesFromDSL = deleteAllNewFilesFromDSL;
//# sourceMappingURL=deleter.js.map