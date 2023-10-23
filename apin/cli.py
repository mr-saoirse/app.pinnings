#!/usr/local/bin/python3
import typer
from apin import logger
from apin.core.ai import kagent
from apin.core.scheduler import start_scheduler

app = typer.Typer()
kagent_app = typer.Typer()
app.add_typer(kagent_app, name="kagent")


scheduler_app = typer.Typer()
app.add_typer(scheduler_app, name="scheduler")


@kagent_app.command("helm")
def run_method(
    prompt: str = typer.Option(None, "--prompt", "-p"),
):
    for filename, contents in kagent.generate_helm_template(prompt):
        with open(filename, "w") as f:
            f.write(contents)


@app.command("build")
def run_method(
    data: str = typer.Option(None, "--data", "-d"),
):
    logger.info(f"Any we're off")


@scheduler_app.command("start")
def scheduler_start():
    logger.info(f"Starting scheduler")
    _ = start_scheduler()


if __name__ == "__main__":
    app()
