import os
import pathlib


class FindNewGenRobots:
    def __init__(self, prev_added_robots):
        # self.generated_files_filepath = pathlib.Path.cwd().parent.parent / "dsl_robotgenerator" \
        self.generated_files_filepath = pathlib.Path.cwd() / "dsl_robotgenerator" \
                                        / "org.gunnarkleiven.robotgenerator.parent" \
                                        / "org.gunnarkleiven.robotgenerator" / "sample" / "src-gen" / "robotgenerator"
        self.prev_added_robots = prev_added_robots

        # print(f"Path = {self.generated_files_filepath}")

    def find_new_generated_robots(self):
        all_generated_robots = os.listdir(self.generated_files_filepath)
        print(f"All generated robots: {all_generated_robots}")
        new_robots = []
        for x in all_generated_robots:
            # If the folder is empty, then the command in the DSL has been deleted, and the folder should be deleted
            # as well
            current_dir = self.generated_files_filepath / x
            if len(os.listdir(current_dir)) == 0:
                print(f"Empty dir: {current_dir}")
                os.removedirs(current_dir)
                continue

            if x not in self.prev_added_robots:
                print(f"Found new generated robot: {x}")
                new_robots.append(x)

        print(f"new_robots: {new_robots}")
        return new_robots
