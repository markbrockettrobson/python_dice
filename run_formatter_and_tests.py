import os
import subprocess
import sys
import typing


def main(run_formatters: bool = False):
    def run_command(command: typing.List[str], env: typing.Optional[typing.Dict[str, str]] = None):
        joined_command = " ".join(command)
        working_env = os.environ.copy()

        if env is None:
            print(f"> {joined_command}")
            subprocess.run(command, check=True, env=working_env, shell=True)
        else:
            for name, value in env.items():
                working_env[name] = value
            print(f"> {joined_command}  {env}")
            subprocess.run(command, check=True, env=working_env, shell=True)

    if run_formatters:
        run_command(["black", "."])
        run_command(["isort", "."])
        run_command(["pytest", "--black", "--isort", "--pylint", "--mypy", "--cov", "."])
    else:
        run_command(["pytest", "."])


if __name__ == "__main__":
    test_only = len(sys.argv) >= 2 and sys.argv[1] == "test_only"
    main(run_formatters=not test_only)
