#!/usr/local/bin/python3
import typer
from apin import logger

app = typer.Typer()


@app.command("build")
def run_method(
    data: str = typer.Option(None, "--data", "-d"),
):
    logger.info(f"Any we're off")


if __name__ == "__main__":
    app()
