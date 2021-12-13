import unittest
import pathlib

from backend.generation_utils.generate_robot import GenerateRobot


class GenerateMooseTestCase(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     cls.generator = GenerateRobot("moose")
    #     print("Finished setup")

    def setUp(self):
        self.generator = GenerateRobot("moose")

    def tearDown(self):
        if not self.generator.save_file.exists():
            self.skipTest("Skipping teardown")
        self.generator.reset_to_default()

    def test_adding_moose_to_world(self):
        # TODO
        pass

    def test_adding_moose_to_config(self):
        # TODO
        pass

    def test_adding_moose_to_data(self):
        # TODO
        pass

    def test_adding_first_moose_controller(self):
        """
        Note, this currently only works when there are no controllers added yet
        """
        new_controller_name = "moose_controller2"
        controllers_filepath = pathlib.Path.cwd().parent / 'controllers' / new_controller_name
        # Check that it does not already exist
        self.assertFalse(controllers_filepath.exists())

        self.generator.add_robot_controller()

        self.assertTrue(controllers_filepath.exists())
        self.assertTrue((controllers_filepath / f'{new_controller_name}.py').exists())
        self.assertTrue((controllers_filepath / "moose_simpleactions2.py").exists())

    def test_resetting_configurations(self):
        # if not self.generator.save_file.exists():
        #     self.skipTest("No save file, hence no controllers added")
        new_controller_name = "moose_controller"
        controller_filepath = pathlib.Path.cwd().parent / 'controllers' / new_controller_name

        self.generator.add_robot_to_world()
        self.generator.add_robot_to_config()
        self.generator.add_robot_to_data()
        self.generator.add_robot_controller()

        # Then do the reset
        self.generator.reset_to_default()

        template_path = pathlib.Path.cwd().parent / 'generation_utils' / 'default_templates'
        world_template = template_path / 'delivery-missionUpdatedTemplate.wbt'
        config_template = template_path / ''




if __name__ == '__main__':
    unittest.main()
