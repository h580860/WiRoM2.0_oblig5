import { ValidationAcceptor, ValidationCheck, ValidationRegistry } from 'langium';
import { RobotGeneratorAstType, Person } from './generated/ast';
import type { RobotGeneratorServices } from './robot-generator-module';

/**
 * Map AST node types to validation checks.
 */
type RobotGeneratorChecks = { [type in RobotGeneratorAstType]?: ValidationCheck | ValidationCheck[] }

/**
 * Registry for validation checks.
 */
export class RobotGeneratorValidationRegistry extends ValidationRegistry {
    constructor(services: RobotGeneratorServices) {
        super(services);
        const validator = services.validation.RobotGeneratorValidator;
        const checks: RobotGeneratorChecks = {
            Person: validator.checkPersonStartsWithCapital
        };
        this.register(checks, validator);
    }
}

/**
 * Implementation of custom validations.
 */
export class RobotGeneratorValidator {

    checkPersonStartsWithCapital(person: Person, accept: ValidationAcceptor): void {
        if (person.name) {
            const firstChar = person.name.substring(0, 1);
            if (firstChar.toUpperCase() !== firstChar) {
                accept('warning', 'Person name should start with a capital.', { node: person, property: 'name' });
            }
        }
    }

}
