package org.gunnarkleiven.robotgenerator.tests;

import com.google.inject.Inject;
import java.util.Map;
import org.eclipse.xtend2.lib.StringConcatenation;
import org.eclipse.xtext.testing.InjectWith;
import org.eclipse.xtext.testing.XtextRunner;
import org.eclipse.xtext.util.IAcceptor;
import org.eclipse.xtext.xbase.lib.Exceptions;
import org.eclipse.xtext.xbase.lib.Extension;
import org.eclipse.xtext.xbase.lib.InputOutput;
import org.eclipse.xtext.xbase.testing.CompilationTestHelper;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(XtextRunner.class)
@InjectWith(RobotgeneratorInjectorProvider.class)
@SuppressWarnings("all")
public class RobotgeneratorGeneratorTest {
  @Inject
  @Extension
  private CompilationTestHelper _compilationTestHelper;
  
  @Test
  public void testGeneratedCodeMultipleFiles() {
    try {
      StringConcatenation _builder = new StringConcatenation();
      _builder.append("addRobot(moose, \"testMoose\",,);");
      _builder.newLine();
      final IAcceptor<CompilationTestHelper.Result> _function = (CompilationTestHelper.Result it) -> {
        StringConcatenation _builder_1 = new StringConcatenation();
        _builder_1.append("# package robotgenerator;");
        _builder_1.newLine();
        _builder_1.append("\t\t\t");
        _builder_1.newLine();
        _builder_1.append("import MooseControllerGenerator");
        _builder_1.newLine();
        _builder_1.append("MooseControllerGenerator(port_number_placeholder, \'mooseName\')");
        _builder_1.newLine();
        Assert.assertEquals(_builder_1.toString(), 
          it.getAllGeneratedResources().get("testMoose.py"));
        InputOutput.<String>print("test");
        InputOutput.<Map<String, CharSequence>>print(it.getAllGeneratedResources());
      };
      this._compilationTestHelper.compile(_builder, _function);
    } catch (Throwable _e) {
      throw Exceptions.sneakyThrow(_e);
    }
  }
}
