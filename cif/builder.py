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


def update_dockerfile(definition_directory: str, image_name: str, previous_tag: str, packages: list[str]):
    if image_name == "_base":
        if not packages:
            return

        with open(os.path.join(definition_directory, "Dockerfile"), "a") as dockerfile:
            dockerfile.write(f"\nRUN apt update && apt install -y {' '.join(packages)} && rm -rf /var/lib/apt/lists/*")
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


def build_docker_image(image_directory: str, image_tag: str, variables: dict[str, str], labels: list[str]) -> None:
    build_args = " ".join([f"--build-arg {variable}={value}" for variable, value in variables.items()])
    build_labels = " ".join([f"--label '{label}'" for label in labels])
    process = subprocess.run(
        f"docker build {build_labels} --tag {image_tag} {build_args} .",
        shell=True,
        cwd=image_directory,
        capture_output=True,
    )
    if process.returncode != 0:
        raise Exception(
            f"Unable to build image {image_tag} from {image_directory}.\n{process.stdout.decode()}\n{process.stderr.decode()}"
        )


def remove_partial_build_images(build_id: str):
    process = subprocess.run(
        f"docker rmi $(docker image ls -q --filter 'label=cif_build={build_id}' --filter 'label=build=partial')",
        shell=True,
        capture_output=True,
    )
    if process.returncode != 0:
        raise Exception(
            f"Unable to prune build images for build {build_id}.\n{process.stdout.decode()}\n{process.stderr.decode()}"
        )


def build_final_docker_image(image_tag: str, previous_tag: str, build_id: str):
    labels = [f"cif_build={build_id}", "build=final"]
    image_directory: str = os.path.join(PATH_BUILD, build_id, "final")
    os.mkdir(image_directory)
    with open(os.path.join(image_directory, "Dockerfile"), "w") as f:
        f.write(f"FROM {previous_tag} AS {image_tag}")
    build_docker_image(image_directory, image_tag, {}, labels)


def image_pipeline(
    build_id: str,
    image_name: str,
    previous_tag: str,
    variables: dict[str, str],
    additional_files: list[tuple[str, str]],
    packages: list[str],
) -> str:
    previous_tag_name = previous_tag.rsplit("/", 1)[1] + "_" if previous_tag else ""
    image_tag = f"{build_id}/{previous_tag_name}{image_name.replace('_', '')}"
    labels = [f"cif_build={build_id}", "build=partial"]
    image_directory = copy_definition(build_id, image_name, additional_files)
    update_dockerfile(image_directory, image_name, previous_tag, packages)
    build_docker_image(image_directory, image_tag, variables, labels)

    return image_tag


def build_services(
    build_id: str, required_images: list[str], variables: dict[str, str], firehole_config: str, packages: list[str]
) -> list[str]:
    services: list[str] = ["_base"] + required_images
    if firehole_config:
        services.append("_firehole")
    image_tags: list[str] = list()
    for service in services:
        additional_files = [(firehole_config, "config.yml")] if service == "_firehole" else []
        previous_tag = image_tags[-1] if image_tags else ""
        tag = image_pipeline(build_id, service, previous_tag, variables, additional_files, packages)
        image_tags.append(tag)

    return image_tags


def copy_action(build_id: str, image_name: str, action_id: str) -> str:
    image_directory: str = os.path.join(PATH_ACTIONS, image_name)
    tmp_image_directory: str = os.path.join(PATH_BUILD, build_id, f"{image_name}-{action_id}")
    shutil.copytree(image_directory, tmp_image_directory)

    return tmp_image_directory


def perform_action(build_id: str, previous_tag: str, action: str, action_id: str, variables: dict[str, str]) -> str:
    new_image_tag = f"{previous_tag}-{action_id}"
    labels = [f"cif_build={build_id}", "build=partial"]
    image_directory = copy_action(build_id, action, action_id)
    update_dockerfile(image_directory, f"{action}-{action_id}", previous_tag, [])
    build_docker_image(image_directory, new_image_tag, variables, labels)

    return new_image_tag


def perform_actions(
    build_id: str, previous_tag: str, action_definitions: list[tuple[str, dict[str, str]]]
) -> list[str]:
    tags = list()
    for action_name, action_variables in action_definitions:
        tags.append(perform_action(build_id, previous_tag, action_name, str(uuid1().fields[0]), action_variables))

    return tags


def build(
    services: list[str],
    variables: dict[str, str],
    actions: list[tuple[str, dict[str, str]]],
    firehole_config: str,
    image_tag: str,
    packages: list[str],
    clean_up: bool = True,
) -> list[str]:
    """
    Build image containing the defined services and actions.
    :param services: Services to add to the final image
    :param variables: Build arguments passed to the docker builder
    :param actions: Actions (and their variables) to add to the final image
    :param firehole_config: Config for Firehole, otherwise it won't run
    :param image_tag: Tag of the final image
    :param packages: Packages to add to the final image
    :param clean_up: Remove all images other than the final one
    :return: All built image tags
    """
    if forbidden_services := check_for_forbidden_services(services):
        raise ValueError(f"Services {forbidden_services} are forbidden.")

    build_id = str(uuid1().fields[0])
    image_tags = build_services(build_id, services, variables, firehole_config, packages)
    image_tags += perform_actions(build_id, image_tags[-1], actions)

    build_final_docker_image(image_tag, image_tags[-1], build_id)
    image_tags.append(image_tag)

    if clean_up:
        remove_partial_build_images(build_id)
        return [image_tag]

    return image_tags
