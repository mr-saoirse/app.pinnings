import json
import re
from apin import logger
from pathlib import Path
import apin
import typing
import subprocess
from apin.core.ops import split_string_with_quotes

# the full repo project with the readme and all
LOCAL_DIR = f"{Path(apin.__file__).parent.parent}"


class GitContext:
    def __init__(
        self, branch="ai.branch", main_branch="main", cwd=None, **kwargs
    ) -> None:
        """
        The Git context manages the agents ability to push code

        """
        self._main_branch = main_branch
        self._origin_uri = "https://github.com/mr-saoirse/thyme"
        self._repo_name = "thyme"
        self._local_dir = LOCAL_DIR or cwd

        self._current_branch = branch or main_branch

        self.get_current_branch()

        logger.debug(f"On branch {self.current_branch}")

    def get_current_branch(self):
        cleaner = lambda s: s.replace("*", "").strip()
        data = self.run_command_list_result("git branch --list")
        self._current_branch = [cleaner(d) for d in data if "*" in d][0]
        return self._current_branch

    def __call__(self, command: str, cwd=None) -> typing.Any:
        return self._run_command(command, cwd=cwd or self._local_dir)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ """

        return False

    @property
    def current_branch(self):
        return self._current_branch

    def get_changes(self, prefix=None, against_origin=False):
        r = (
            self("git diff --name-only")
            if not against_origin
            else self("git diff --name-only origin/main")
        )
        changes = r["data"]
        changes = [c for c in changes if c != ""]
        if prefix:
            return [c for c in changes if c[: len(prefix)] == prefix if c != ""]
        return changes

    def rebase_main(self, branch=None):
        """
        We always have the parent root to where we clone things
        and if we know the name of the
        """
        branch = branch or self._current_branch
        self.commit_all()
        self(f"git checkout main")
        self(f"git fetch")
        self(f"git pull")
        self(f"git checkout {branch}")
        self("git rebase main")

    def push(
        self, pr_name="AI Pushed", pr_change_note="AI comments TODO", auto_merge=True
    ):
        """ """

        logger.info(f"Committing from branch {self._current_branch}")
        self.rebase_main()
        # TODO:> todo determine what branch we are actually meaning to be on
        self(f"git rebase origin/{self._main_branch}")

        # TODO: here we assume the provider is github so we need to generalize this part
        self(f"git push origin {self._current_branch} --force")
        self(f"""gh pr create --title "{pr_name}" --body "{pr_change_note}" """)
        if auto_merge:
            self("gh pr merge --auto --rebase")
            logger.info(f"Pushed pr [{pr_name}] and auto merged (pending checks)")
        else:
            logger.info(f"Pushed pr [{pr_name}] needs review")

    def commit_all(self, message=None):
        # for testing only - we can test the flow without changes
        # self("touch file.txt")
        message = message or "automated commit"
        self("git add .")
        chk = self(f'git commit -m "{message}"')
        # TODO: check if managed to commit the changes
        changes = self.get_changes()

        return changes

    def run_command_single_result(self, command):
        r = self(command)
        if r["status"] == "ok":
            return r["data"][0]
        raise Exception(f"Command failed {r['data']}")

    def run_command_list_result(self, command):
        r = self(command)
        if r["status"] == "ok":
            return r["data"]
        raise Exception(f"Command failed {r['data']}")

    def _run_command(self, command, cwd=None):
        # this does not always work but we are using this convention
        options = split_string_with_quotes(command)
        logger.debug(f"running command {command} in {cwd}")

        process = subprocess.Popen(
            options, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd
        )

        status = "ok"
        out, err = process.communicate()

        if process.returncode and err:
            out = err
            status = "error"
            logger.warning(f"process-> {out}")
        elif out:
            logger.debug(out)

        return {"status": status, "data": out.decode().split("\n")}
