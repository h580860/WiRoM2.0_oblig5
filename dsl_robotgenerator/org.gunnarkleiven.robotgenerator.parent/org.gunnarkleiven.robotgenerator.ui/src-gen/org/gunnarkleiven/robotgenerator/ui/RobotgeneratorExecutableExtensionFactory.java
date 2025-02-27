/*
 * generated by Xtext 2.25.0
 */
package org.gunnarkleiven.robotgenerator.ui;

import com.google.inject.Injector;
import org.eclipse.xtext.ui.guice.AbstractGuiceAwareExecutableExtensionFactory;
import org.gunnarkleiven.robotgenerator.ui.internal.RobotgeneratorActivator;
import org.osgi.framework.Bundle;
import org.osgi.framework.FrameworkUtil;

/**
 * This class was generated. Customizations should only happen in a newly
 * introduced subclass. 
 */
public class RobotgeneratorExecutableExtensionFactory extends AbstractGuiceAwareExecutableExtensionFactory {

	@Override
	protected Bundle getBundle() {
		return FrameworkUtil.getBundle(RobotgeneratorActivator.class);
	}
	
	@Override
	protected Injector getInjector() {
		RobotgeneratorActivator activator = RobotgeneratorActivator.getInstance();
		return activator != null ? activator.getInjector(RobotgeneratorActivator.ORG_GUNNARKLEIVEN_ROBOTGENERATOR_ROBOTGENERATOR) : null;
	}

}
