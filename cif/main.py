import os
import shutil
from uuid import uuid1
from argparse import ArgumentParser
import subprocess


PATH_BASE = os.path.dirname(__file__).rsplit("/", 1)[0]
PATH_IMAGES = os.path.join(PATH_BASE, "images")
PATH_ACTIONS = os.path.join(PATH_BASE, "actions")
PATH_BUILD = os.path.join(PATH_BASE, ".build")


def copy_image(build_id: str, image_name: str, firehole_config: str) -> str:
    image_directory: str = os.path.join(PATH_IMAGES, image_name)
    tmp_image_directory: str = os.path.join(PATH_BUILD, build_id, image_name)
    shutil.copytree(image_directory, tmp_image_directory)
    if firehole_config:
        shutil.copyfile(firehole_config, os.path.join(tmp_image_directory, "config.yml"))

    return tmp_image_directory


def update_image(image_directory: str, image_name: str, previous_tag: str):
    if image_name == "_base":
        return

    with open(os.path.join(image_directory, "Dockerfile")) as dockerfile:
        lines = dockerfile.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith("FROM"):
                lines[i] = line.replace("base", previous_tag)
            if line.startswith("COPY entrypoint.sh /entrypoints"):
                lines[i] = line.replace("/entrypoints", f"/entrypoints/entrypoint-{image_name}.sh")

    with open(os.path.join(image_directory, "Dockerfile"), "w") as dockerfile:
        dockerfile.writelines(lines)


def build_image(image_directory: str, image_tag: str, variables: dict[str, str]):
    build_args = " ".join([f"--build-arg {variable}={value}" for variable, value in variables.items()])
    process = subprocess.run(f"docker build --tag {image_tag} {build_args} .", shell=True, cwd=image_directory, capture_output=True)
    if process.returncode != 0:
        raise Exception(f"Unable to build image {image_tag} from {image_directory}.\n{process.stdout.decode()}\n{process.stderr.decode()}")


def image_pipeline(repository: str, build_id: str, image_name: str, previous_tag: str, variables: dict[str, str], firehole_config: str) -> str:
    previous_tag_name = previous_tag.rsplit("/", 1)[1] + "_" if previous_tag else ""
    image_tag = f"{repository}{'' if repository.endswith('/') else '/'}{previous_tag_name}{image_name.replace('_', '')}"
    image_directory = copy_image(build_id, image_name, firehole_config if image_name == "firehole" else "")
    update_image(image_directory, image_name, previous_tag)
    build_image(image_directory, image_tag, variables)

    return image_tag


def build_images(build_id: str, image_repository: str, required_images: list[str], variables: dict[str, str], firehole_config: str) -> str:
    images: list[str] = ["_base"] + required_images
    image_tags: list[str] = list()
    for image in images:
        print(f"Building image {image}.. ")
        tag = image_pipeline(image_repository, build_id, image, image_tags[-1] if len(image_tags) > 0 else "", variables, firehole_config)
        image_tags.append(tag)
        print("Success.")
        print(f"Tagged as {tag}\n")

    return image_tags[-1]


def parse_image_variables(variables_raw: list[str]) -> dict[str, str]:
    return dict(variable.split("=", 1) for variable in variables_raw)

def copy_action(build_id: str, image_name: str, action_id: str) -> str:
    image_directory: str = os.path.join(PATH_ACTIONS, image_name)
    tmp_image_directory: str = os.path.join(PATH_BUILD, build_id, f"{image_name}-{action_id}")
    shutil.copytree(image_directory, tmp_image_directory)

    return tmp_image_directory


def perform_action(build_id: str, tag: str, action: str, action_id: str, variables: dict[str, str]):
    image_directory = copy_action(build_id, action, action_id)
    update_image(image_directory, f"{action}-{action_id}", tag)
    build_image(image_directory, tag, variables)


def perform_actions(build_id: str, tag: str, action_definitions: list[tuple[str, dict[str, str]]]):
    # Add each action details to the image tags/description
    for action_name, action_variables in action_definitions:
        print(f"Applying action {action_name}.. ")
        perform_action(build_id, tag, action_name, str(uuid1()), action_variables)
        print("Success.")
        print(f"Tagged as {tag}\n")


def parse_actions(action_definitions: list[str]) -> list[tuple[str, dict[str, str]]]:
    parsed_actions: list[tuple[str, dict[str, str]]] = list()
    for action in action_definitions:
        action_name, action_variables_raw = action.split(":", 1)
        action_variables = dict(variable.split("=", 1) for variable in action_variables_raw.split(","))
        parsed_actions.append((action_name, action_variables))

    return parsed_actions


def main():
    parser = ArgumentParser()
    parser.add_argument("images", nargs="*")
    parser.add_argument("-v", "--variable", action='append', default=list(), help="Variable for images. (MY_VAR=var)")
    parser.add_argument("-fc", "--firehole-config")
    parser.add_argument("-r", "--repository", default="cif")
    parser.add_argument("-a", "--action", action='append', default=list(), help="Action with variables. (create-user:USER_NAME=user,USER_PASSWORD=user)")
    required_images = parser.parse_args().images
    variables_override = parser.parse_args().variable
    actions = parser.parse_args().action
    firehole_config = parser.parse_args().firehole_config
    image_repository = parser.parse_args().repository

    build_id = str(uuid1())
    parsed_image_variables = parse_image_variables(variables_override)
    final_tag = build_images(build_id, image_repository, required_images, parsed_image_variables, firehole_config)
    parsed_actions = parse_actions(actions)
    perform_actions(build_id, final_tag, parsed_actions)
