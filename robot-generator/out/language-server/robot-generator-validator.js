"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.RobotGeneratorValidator = exports.RobotGeneratorValidationRegistry = void 0;
const langium_1 = require("langium");
/**
 * Registry for validation checks.
 */
class RobotGeneratorValidationRegistry extends langium_1.ValidationRegistry {
    constructor(services) {
        super(services);
        const validator = services.validation.RobotGeneratorValidator;
        const checks = {
            Person: validator.checkPersonStartsWithCapital
        };
        this.register(checks, validator);
    }
}
exports.RobotGeneratorValidationRegistry = RobotGeneratorValidationRegistry;
/**
 * Implementation of custom validations.
 */
class RobotGeneratorValidator {
    checkPersonStartsWithCapital(person, accept) {
        if (person.name) {
            const firstChar = person.name.substring(0, 1);
            if (firstChar.toUpperCase() !== firstChar) {
                accept('warning', 'Person name should start with a capital.', { node: person, property: 'name' });
            }
        }
    }
}
exports.RobotGeneratorValidator = RobotGeneratorValidator;
//# sourceMappingURL=robot-generator-validator.js.map