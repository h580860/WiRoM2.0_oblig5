import unittest
import pathlib

from backend.generation_utils.generate_moose import GenerateMoose


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.moose_generator = GenerateMoose()
        print("Finished setup once")

    def test_succeed(self):
        # self.assertEqual(True, False)  # add assertion here
        self.assertEqual(True, True)

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

        self.moose_generator.test_adding_moose_controller()

        self.assertTrue(controllers_filepath.exists())
        self.assertTrue((controllers_filepath / f'{new_controller_name}.py').exists())
        self.assertTrue((controllers_filepath / "moose_simpleactions2.py").exists())

    def test_resetting_configurations(self):
        # TODO
        pass


if __name__ == '__main__':
    unittest.main()
