import subprocess
import pathlib
import os
import time


class DSLShellCommands:
    # def __init__(self, script_path, filepath):
    def __init__(self, filepath):
        #self.script_path = script_path
        self.filepath = filepath

    def test(self):
        subprocess.run(["./../../robot-generator/bin/cli", "help", "generate"])

    def test2(self):
        subprocess.run(["./../../robot-generator/bin/cli", "generate",
                        f"{self.filepath}/example/testDsl.robotgenerator", "-d", f"{self.filepath}/example/generated"])

    def generate_dsl_code_command(self):
        # subprocess.run("./bin/cli generate example/testDsl.robotgenerator")
        # TODO this was written on Mac OS, there might be a different way to call
        # the ./bin/cli on another operating system
        # subprocess.run([".", "../../robot-generator/bin/cli"])
        # res = subprocess.run(["./robot-generator/bin/cli", "generate", f"{self.filepath}/example/testDsl.robotgenerator",
        #                      "-d", f"{self.filepath}/example/generated"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        res = subprocess.run(["./robot-generator/bin/cli", "generate", f"{self.filepath}/example/testDsl.robotgenerator",
                             "-d", f"{self.filepath}/example/generated"], capture_output=True, text=True)

        # subprocess.run(["./../../robot-generator/bin/cli", "generate",
        #                f"{self.filepath}/example/testDsl.robotgenerator"])
        # print(f"res  = {res}")
        print(f"stdout: {res.stdout}")
        print(f"stderr: {res.stderr}")
        print(f"returncode: {res.returncode}")

        return res

        # subprocess.run([f"./{self.filepath}/bin/cli", "generate", f"{self.filepath}example/testDsl.robotgenerator"])

    def delete_generated_files_command(self):
        res = subprocess.run(["./robot-generator/bin/cli",
                              "delete", f"{self.filepath}/example/generated"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # subprocess.run(["./../../robot-generator/bin/cli", "delete"])
        print(f"stdout: {res.stdout}")
        print(f"stderr: {res.stderr}")
        print(f"returncode: {res.returncode}")

        return res


if __name__ == '__main__':
    # dsl_filepath = "example/testDsl.robotgenerator"
    dsl_filepath = \
        pathlib.Path(os.getcwd()).parent.parent / "robot-generator"

    # print(dsl_filepath)
    shell_commands = DSLShellCommands(dsl_filepath)
    # shell_commands.generate_dsl_code_command()
    shell_commands.delete_generated_files_command()
    # shell_commands.test2()
