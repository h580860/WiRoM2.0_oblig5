"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteAllNewFilesFromDSL = void 0;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
// import colors from 'colors';
// // import { CompositeGeneratorNode, NL, processGeneratorNode } from 'langium';
// import { CompositeGeneratorNode, processGeneratorNode } from 'langium';
// import path from 'path';
// import { DslCommand } from '../language-server/generated/ast';
// import { extractDestinationAndName } from './cli-util';
function deleteAllNewFilesFromDSL(filePath, destination) {
    // const data = extractDestinationAndName(filePath, destination);
    if (fs_1.default.existsSync(filePath)) {
        // Source: https://stackoverflow.com/questions/27072866/how-to-remove-all-files-from-directory-without-removing-directory-in-node-js
        fs_1.default.readdir(filePath, (err, files) => {
            if (err)
                throw err;
            for (const file of files) {
                fs_1.default.unlink(path_1.default.join(filePath, file), err => {
                    if (err)
                        throw err;
                });
            }
        });
    }
    else {
        console.log(`${filePath} does not exist`);
        return;
    }
}
exports.deleteAllNewFilesFromDSL = deleteAllNewFilesFromDSL;
//# sourceMappingURL=deleter.js.map