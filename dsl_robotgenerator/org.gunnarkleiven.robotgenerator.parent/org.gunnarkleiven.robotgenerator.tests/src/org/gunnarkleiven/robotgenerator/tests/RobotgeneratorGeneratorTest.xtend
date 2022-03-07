package org.gunnarkleiven.robotgenerator.tests

import com.google.inject.Inject
import org.eclipse.xtext.testing.InjectWith
import org.eclipse.xtext.testing.XtextRunner
import org.eclipse.xtext.testing.util.ParseHelper
import org.eclipse.xtext.testing.validation.ValidationTestHelper
import org.gunnarkleiven.robotgenerator.robotgenerator.Model
import org.gunnarkleiven.robotgenerator.robotgenerator.RobotType
import org.junit.runner.RunWith
import org.junit.Test
import org.eclipse.xtext.xbase.testing.CompilationTestHelper

import static extension org.junit.Assert.*

@RunWith(XtextRunner)
@InjectWith(RobotgeneratorInjectorProvider)
class RobotgeneratorGeneratorTest {
	
	@Inject extension CompilationTestHelper
	
//	@Test
//	def void testGeneratedCode() {
//		'''
//		addRobot(moose, "testName", 3, 4);
//		'''.assertCompilesTo(
//			'''
//			# package robotgenerator;
//			
//			import MooseSimpleactionsGenerator
//			MooseSimpleactionsGenerator(port_number_placeholder, 'testName')
//			'''
//		)
//	}
//	
//	
//	
//	@Test
//	def void testGeneratedCode2() {
//		'''
//		addRobot(mavic2pro, "mavicname",,)
//		'''.assertCompilesTo(
//			'''
//			# package robotgenerator;
//			
//			import Mavic2proSimpleactionsGenerator
//			Mavic2proSimpleactionsGenerator(port_number_placeholder, 'mavicname')
//			'''
//		)
//	}
	
	@Test
	def void testGeneratedCodeMultipleFiles() {
		'''
		addRobot(moose, "testMoose",,);
		'''.compile [
			'''
			# package robotgenerator;
						
			import MooseSimpleactionsGenerator
			MooseSimpleactionsGenerator(port_number_placeholder, 'mooseName')
			'''.toString.assertEquals(
				getAllGeneratedResources.get("testMoose.py")
			)
			print("test")
			print(getAllGeneratedResources)
			
//			'''
//			"moose": {
//				"name": "mooseName",
//				"location": {
//					"x": "undefined",
//					"y": "undefined"
//				}
//			}
//			'''.toString.assertEquals(getGeneratedCode("mooseName.json"))
		]
	}
	
}