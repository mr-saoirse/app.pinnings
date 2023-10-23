import openai
from apin import logger
from apin.core.ops import parse_fenced_code_blocks
from apin import STACK_HOME
from pathlib import Path


def generate_application_set(instruction, name=None, path=None, **kwargs):
    prompt = """
    Generate an Argo Application Set YAML file as requested.
    the cluster should be
    """
    result = file_gen(prompt, instruction)

    return result


def generate_applications(instruction, name=None, path=None, **kwargs):
    prompt = """
    Generate files in a single YAML file.
    """
    result = file_gen(prompt, instruction)

    return result


def generate_helm_template(instruction, name=None, path=None, **kwargs):
    prompt = """
    Generate a full set of HELM template files with a values.yaml. 
    Allow for configuration of the image and resources plus anything else the user asks. 
    The user will specify what type of kubernetes application they want.
    As we need to use Kustomize with this, you should add the kustomization setup for modifying the docker image.
    add metadata labels saying AI generates the objects and also Open Telemetry hooks if you can.
    """
    result = file_gen(prompt, instruction)

    return result


# def add_operator_subscription(instruction, name=None, path=None, **kwargs):
#     prompt = """

#     """
#     result = file_gen(prompt, instruction)
#     logger.info(result)
#     return result


def file_gen(prompt, hints, model="gpt-4"):
    # Provide a JSON dictionary with file name and file text content as a result.
    messages = [
        {
            "role": "system",
            "content": f"""You are a file generator for Kubernetes YAML files for use in different contexts. {prompt}.""",
        },
        {
            "role": "user",
            "content": hints,
        },
        {
            "role": "user",
            "content": """use the following result format with JSON for header info and then a list of files in fenced YAML:
             ```json { "files" : ["file1.yaml", "file2.yaml", "file3.yaml", "file4.yaml", ....] }```
             ```yaml FILE 1 CONTENTS```
             ```yaml FILE 2 CONTENTS```
             ```yaml FILE 3 CONTENTS```
             ```yaml FILE 4 CONTENTS```
             etc.
            """,
        },
    ]

    logger.debug(f"Generating. Please wait a moment...")
    response = openai.ChatCompletion.create(model=model, messages=messages)

    results = response["choices"][0]["message"]["content"]
    logger.info(results)

    try:
        json_data = parse_fenced_code_blocks(results, select_type="json")
        yaml_data = parse_fenced_code_blocks(results, select_type="yaml")

        json_data = json_data[0].get("files")
        data = dict(zip(json_data, yaml_data))

        for k, v in data.items():
            file = f"{STACK_HOME}/test/{k}"
            logger.info(f"Writing {file}")
            Path(Path(file).parent).mkdir(exist_ok=True, parents=True)
            with open(file, "w") as f:
                f.write(v)
    except Exception as ex:
        logger.error(f"Failing to parse {ex}")
        return results
    return data
