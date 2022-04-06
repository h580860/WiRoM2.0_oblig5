import fs from 'fs';
import path from 'path';
import colors from 'colors';
// // import { CompositeGeneratorNode, NL, processGeneratorNode } from 'langium';
// import { CompositeGeneratorNode, processGeneratorNode } from 'langium';
// import path from 'path';
// import { DslCommand } from '../language-server/generated/ast';
import { extractDestinationAndName } from './cli-util';

export function deleteAllNewFilesFromDSL(filePath: string, destination: string | undefined): void {
    const data = extractDestinationAndName(filePath, destination);

    // console.log(`Destination: ${data.destination}, name: ${data.name}`);
    if (fs.existsSync(data.destination)) {
        // Source: https://stackoverflow.com/questions/27072866/how-to-remove-all-files-from-directory-without-removing-directory-in-node-js

        fs.readdir(data.destination, (err, files) => {
            if (err) throw err;

            for (const file of files) {
                fs.unlink(path.join(data.destination, file), err => {
                    if (err) throw err;
                })
            }
        })
    }
    console.log(colors.green(`Finished deleting files in ${data.destination}`));
}
