package org.gunnarkleiven.robotgenerator.tests;

import com.google.inject.Inject;
import org.eclipse.xtend2.lib.StringConcatenation;
import org.eclipse.xtext.testing.InjectWith;
import org.eclipse.xtext.testing.XtextRunner;
import org.eclipse.xtext.testing.util.ParseHelper;
import org.eclipse.xtext.testing.validation.ValidationTestHelper;
import org.eclipse.xtext.xbase.lib.Exceptions;
import org.eclipse.xtext.xbase.lib.Extension;
import org.gunnarkleiven.robotgenerator.robotgenerator.Model;
import org.gunnarkleiven.robotgenerator.robotgenerator.RobotgeneratorPackage;
import org.gunnarkleiven.robotgenerator.validation.RobotgeneratorValidator;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(XtextRunner.class)
@InjectWith(RobotgeneratorInjectorProvider.class)
@SuppressWarnings("all")
public class RobotgeneratorValidatorTest {
  @Inject
  @Extension
  private ParseHelper<Model> _parseHelper;
  
  @Inject
  @Extension
  private ValidationTestHelper _validationTestHelper;
  
  @Test
  public void testIllegalRobotName() {
    try {
      StringConcatenation _builder = new StringConcatenation();
      _builder.append("addRobot(moose, \"moose\",,);");
      _builder.newLine();
      this._validationTestHelper.assertError(this._parseHelper.parse(_builder), 
        RobotgeneratorPackage.eINSTANCE.getCommand(), 
        RobotgeneratorValidator.ILLEGAL_ROBOT_NAME, 
        "Protected robot name \'moose\'");
    } catch (Throwable _e) {
      throw Exceptions.sneakyThrow(_e);
    }
  }
  
  @Test
  public void testValidCommand() {
    try {
      StringConcatenation _builder = new StringConcatenation();
      _builder.append("addRobot(moose, \"moose3\", 3, 3);");
      _builder.newLine();
      this._validationTestHelper.assertNoErrors(this._parseHelper.parse(_builder));
    } catch (Throwable _e) {
      throw Exceptions.sneakyThrow(_e);
    }
  }
}
