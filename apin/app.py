from fastapi import FastAPI, APIRouter
import typing
from apin.core.types import ChangeSet


app = FastAPI()
api_router = APIRouter()
PROCESS_NAME = "kagent"


@app.get("/")
@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@app.get(f"/{PROCESS_NAME}/")
def say_hi():
    return {"message": "Hello, World"}


@api_router.get(f"/{PROCESS_NAME}/changes", status_code=200, response_model=dict)
def process_changes(
    *, repo: str, sha: str, changes: typing.List[ChangeSet], branch_prefix="cluster"
) -> dict:
    """
    Process changes from the repo

    - fetch the repo
    - build the manifests for the sha
    - create a branch with the prefix + hash - prune auto
    - push back the changes to the branch which argo picks up
    """

    return {}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8008)
