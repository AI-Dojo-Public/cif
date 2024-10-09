import os
import shutil
from uuid import uuid1
import subprocess

from cif.settings import PATH_SERVICES, PATH_ACTIONS, PATH_BUILD
from cif.helpers import check_for_forbidden_services


def copy_definition(build_id: str, image_name: str, additional_files: list[tuple[str, str]] = None) -> str:
    image_directory: str = os.path.join(PATH_SERVICES, image_name)
    tmp_image_directory: str = os.path.join(PATH_BUILD, build_id, image_name)
    shutil.copytree(image_directory, tmp_image_directory)

    for file_path, file_new_name in additional_files if additional_files else []:
        shutil.copyfile(file_path, os.path.join(tmp_image_directory, file_new_name))

    return tmp_image_directory


def update_dockerfile(definition_directory: str, image_name: str, previous_tag: str):
    if image_name == "_base":
        return

    with open(os.path.join(definition_directory, "Dockerfile")) as dockerfile:
        lines = dockerfile.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith("FROM"):
                lines[i] = line.replace("base", previous_tag)
            if line.startswith("COPY entrypoint.sh /entrypoints"):
                lines[i] = line.replace("/entrypoints", f"/entrypoints/entrypoint-{image_name}.sh")

    with open(os.path.join(definition_directory, "Dockerfile"), "w") as dockerfile:
        dockerfile.writelines(lines)


def build_docker_image(image_directory: str, image_tag: str, variables: dict[str, str]):
    build_args = " ".join([f"--build-arg {variable}={value}" for variable, value in variables.items()])
    process = subprocess.run(
        f"docker build --tag {image_tag} {build_args} .", shell=True, cwd=image_directory, capture_output=True
    )
    if process.returncode != 0:
        raise Exception(
            f"Unable to build image {image_tag} from {image_directory}.\n{process.stdout.decode()}\n{process.stderr.decode()}"
        )


def tag_docker_image(old_tag: str, new_tag: str):
    process = subprocess.run(f"docker tag {old_tag} {new_tag}", shell=True, capture_output=True)
    if process.returncode != 0:
        raise Exception(
            f"Unable to tag create tag {new_tag} from {old_tag}.\n{process.stdout.decode()}\n{process.stderr.decode()}"
        )


def image_pipeline(
    repository: str,
    build_id: str,
    image_name: str,
    previous_tag: str,
    variables: dict[str, str],
    additional_files: list[tuple[str, str]],
) -> str:
    previous_tag_name = previous_tag.rsplit("/", 1)[1] + "_" if previous_tag else ""
    image_tag = f"{repository}{previous_tag_name}{image_name.replace('_', '')}"
    image_directory = copy_definition(build_id, image_name, additional_files)
    update_dockerfile(image_directory, image_name, previous_tag)
    build_docker_image(image_directory, image_tag, variables)

    return image_tag


def build_services(
    build_id: str, image_repository: str, required_images: list[str], variables: dict[str, str], firehole_config: str
) -> list[str]:
    services: list[str] = ["_base"] + required_images
    if firehole_config:
        services.append("_firehole")
    image_tags: list[str] = list()
    for service in services:
        additional_files = [(firehole_config, "config.yml")] if service == "_firehole" else []
        previous_tag = image_tags[-1] if image_tags else ""
        tag = image_pipeline(image_repository, build_id, service, previous_tag, variables, additional_files)
        image_tags.append(tag)

    return image_tags


def copy_action(build_id: str, image_name: str, action_id: str) -> str:
    image_directory: str = os.path.join(PATH_ACTIONS, image_name)
    tmp_image_directory: str = os.path.join(PATH_BUILD, build_id, f"{image_name}-{action_id}")
    shutil.copytree(image_directory, tmp_image_directory)

    return tmp_image_directory


def perform_action(build_id: str, previous_tag: str, action: str, action_id: str, variables: dict[str, str]) -> str:
    new_image_tag = f"{previous_tag}-{action_id}"
    image_directory = copy_action(build_id, action, action_id)
    update_dockerfile(image_directory, f"{action}-{action_id}", previous_tag)
    build_docker_image(image_directory, new_image_tag, variables)

    return new_image_tag


def perform_actions(
    build_id: str, previous_tag: str, action_definitions: list[tuple[str, dict[str, str]]]
) -> list[str]:
    tags = list()
    for action_name, action_variables in action_definitions:
        tags.append(perform_action(build_id, previous_tag, action_name, str(uuid1().fields[0]), action_variables))

    return tags


def build(
    repository: str,
    services: list[str],
    variables: dict[str, str],
    actions: list[tuple[str, dict[str, str]]],
    firehole_config: str,
    image_tag: str | None,
) -> list[str]:
    """
    Build image containing the defined services and actions.
    :param repository: Docker image repository (image prefix)
    :param services: Services to add to the final image
    :param variables: Build arguments passed to the docker builder
    :param actions: Actions (and their variables) to add to the final image
    :param firehole_config: Config for Firehole, otherwise it won't run.
    :param image_tag: Tag of the final image
    :return: All built image tags
    """
    if forbidden_services := check_for_forbidden_services(services):
        raise ValueError(f"Services {forbidden_services} are forbidden.")

    build_id = uuid1().fields[0]
    repository = f"{repository}{'' if repository.endswith('/') else '/'}{build_id}/"
    image_tags = build_services(str(build_id), repository, services, variables, firehole_config)
    image_tags += perform_actions(str(build_id), image_tags[-1], actions)
    if image_tag:
        tag_docker_image(image_tags[-1], image_tag)
        image_tags.append(image_tag)

    return image_tags
