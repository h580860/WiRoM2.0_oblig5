import fs from 'fs';
import path from 'path';
import colors from 'colors';
// // import { CompositeGeneratorNode, NL, processGeneratorNode } from 'langium';
// import { CompositeGeneratorNode, processGeneratorNode } from 'langium';
// import path from 'path';
// import { DslCommand } from '../language-server/generated/ast';
// import { extractDestinationAndName } from './cli-util';

export function deleteAllNewFilesFromDSL(filePath: string, destination: string | undefined): void {
    // const data = extractDestinationAndName(filePath, destination);

    if (fs.existsSync(filePath)) {
        // Source: https://stackoverflow.com/questions/27072866/how-to-remove-all-files-from-directory-without-removing-directory-in-node-js
        fs.readdir(filePath, (err, files) => {
            if (err) throw err;

            for (const file of files) {
                fs.unlink(path.join(filePath, file), err => {
                    if (err) throw err;
                })
            }
        })
    }
    else {
        console.log(colors.red(`${filePath} does not exist`));
        return
    }

}
