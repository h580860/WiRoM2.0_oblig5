package org.gunnarkleiven.robotgenerator.tests

import com.google.inject.Inject
import org.eclipse.xtext.testing.InjectWith
import org.eclipse.xtext.testing.XtextRunner
import org.eclipse.xtext.testing.util.ParseHelper
import org.eclipse.xtext.testing.validation.ValidationTestHelper
import org.gunnarkleiven.robotgenerator.robotgenerator.Model
import org.gunnarkleiven.robotgenerator.robotgenerator.RobotType
import org.gunnarkleiven.robotgenerator.validation.RobotgeneratorValidator
import org.junit.runner.RunWith
import org.junit.Test
import org.junit.Assert
import org.gunnarkleiven.robotgenerator.robotgenerator.RobotgeneratorPackage

@RunWith(XtextRunner)
@InjectWith(RobotgeneratorInjectorProvider)
class RobotgeneratorValidatorTest {
	
	@Inject extension ParseHelper<Model>
	@Inject extension ValidationTestHelper
	
	@Test
	def testIllegalRobotName() {
		'''
		addRobot(moose, "moose",,);
		'''.parse.assertError(
			RobotgeneratorPackage.eINSTANCE.command,
			RobotgeneratorValidator.ILLEGAL_ROBOT_NAME,
			"Protected robot name 'moose'"
		)
	}
	
	@Test
	def testValidCommand() {
		'''
		addRobot(moose, "moose3", 3, 3);
		'''.parse.assertNoErrors
	}
	
	// TODO fix this test
//	@Test
//	def testValidRobotType() {
//		'''
//		addRobot(mose, , , );
//		'''.parse.assertError(
//			RobotgeneratorPackage.eINSTANCE.command,
//			RobotgeneratorValidator.INVALID_ROBOT_TYPE,
//			"Invalid robot type: 'mose'"
//		)
//	}
	
//	@Test
//	def testDuplicateRobotnames() {
//		'''
//		addRobot(moose, "moose1",1,3);
//		addRobot(moose, "moose1", 1,4);
//		'''.parse.assertError(
//			RobotgeneratorPackage.eINSTANCE.command,
//			RobotgeneratorValidator.DUPLICATE_ROBOT_NAMES,
//			"Duplicate robot name: 'moose1'"
//		)
//	}
}