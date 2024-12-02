import os
import shutil
from uuid import uuid1
import subprocess

from cif.settings import PATH_SERVICES, PATH_ACTIONS, PATH_BUILD
from cif.helpers import check_for_forbidden_services, FileCopy


def copy_definition(build_id: str, image_name: str) -> str:
    image_directory: str = os.path.join(PATH_SERVICES, image_name)
    tmp_image_directory: str = os.path.join(PATH_BUILD, build_id, image_name)
    shutil.copytree(image_directory, tmp_image_directory)

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
        f"docker image ls -q --filter 'label=cif_build={build_id}' --filter 'label=build=partial'",
        shell=True,
        capture_output=True,
    )
    if process.returncode != 0:
        raise Exception(
            f"Unable to list build images for build {build_id}.\n{process.stdout.decode()}\n{process.stderr.decode()}"
        )

    images = process.stdout.decode().split("\n")
    process = subprocess.run(
        f"docker rmi {' '.join(images)}",
        shell=True,
        capture_output=True,
    )
    if process.returncode != 0:
        raise Exception(
            f"Unable to prune build images for build {build_id}.\n{process.stdout.decode()}\n{process.stderr.decode()}"
        )


def create_tmp_files(files: list[FileCopy], image_directory: str) -> list[str]:
    tmp_files_directory: str = os.path.join(image_directory, "files")
    os.mkdir(tmp_files_directory)
    instructions: list[str] = list()

    for host_path, image_path, user, group, mode in files:
        destination: str = shutil.copy2(host_path, tmp_files_directory)
        context_destination = destination.removeprefix(image_directory)
        chmod = f"--chmod={mode}" if mode else ""
        chown = f"--chown={user if user else ''}{f':{group}' if group else ''}"
        instructions.append(f"COPY {chown} {chmod} {context_destination} {image_path}\n")

    return instructions


def build_final_docker_image(image_tag: str, previous_tag: str, build_id: str, files: list[FileCopy]):
    labels = [f"cif_build={build_id}", "build=final"]
    image_directory: str = os.path.join(PATH_BUILD, build_id, "final")
    os.mkdir(image_directory)
    copy_files_instructions = create_tmp_files(files, image_directory)

    with open(os.path.join(image_directory, "Dockerfile"), "w") as docker_file:
        docker_file.write(f"FROM {previous_tag} AS {image_tag}\n")
        docker_file.writelines(copy_files_instructions)
    build_docker_image(image_directory, image_tag, {}, labels)


def image_pipeline(
    build_id: str, image_name: str, previous_tag: str, variables: dict[str, str], packages: list[str]
) -> str:
    previous_tag_name = previous_tag.rsplit("/", 1)[1] + "_" if previous_tag else ""
    image_tag = f"{build_id}/{previous_tag_name}{image_name.replace('_', '')}"
    labels = [f"cif_build={build_id}", "build=partial"]
    image_directory = copy_definition(build_id, image_name)
    update_dockerfile(image_directory, image_name, previous_tag, packages)
    build_docker_image(image_directory, image_tag, variables, labels)

    return image_tag


def build_services(build_id: str, services: list[str], variables: dict[str, str], packages: list[str]) -> list[str]:
    image_tags: list[str] = list()
    for service in services:
        previous_tag = image_tags[-1] if image_tags else ""
        tag = image_pipeline(build_id, service, previous_tag, variables, packages)
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
    final_tag: str,
    packages: list[str],
    files: list[FileCopy],
    clean_up: bool = True,
) -> list[str]:
    """
    Build image containing the defined services and actions.

    The `files` parameter takes:
    host_path: File path on the host system
    image_path: File path on the image
    username: username or UID to change as the owner of the file (uses Docker's chown)
    groupname: groupname or GID to change as the owner of the file (uses Docker's chown)
    mode: Set file permission bits (uses Docker's chmod)
    More information can be found in the Docker documentation https://docs.docker.com/reference/dockerfile/#copy.

    :param services: Services to add to the final image
    :param variables: Build arguments passed to the docker builder
    :param actions: Actions (and their variables) to add to the final image
    :param firehole_config: Config for Firehole, otherwise it won't run
    :param final_tag: Tag of the final image
    :param packages: Packages to add to the final image
    :param files: Files to add to the final image (host_path, image_path, username, groupname, mode)
    :param clean_up: Remove all artifacts from the build (tmp images, tmp files)
    :return: All built image tags
    """
    if forbidden_services := check_for_forbidden_services(services):
        raise ValueError(f"Services {forbidden_services} are forbidden.")

    services = ["_base"] + services
    if firehole_config:
        services.append("_firehole")
        files.append((firehole_config, "/firehole-config.yml", None, None, None))

    build_id = str(uuid1().fields[0])
    image_tags = build_services(build_id, services, variables, packages)
    image_tags += perform_actions(build_id, image_tags[-1], actions)

    build_final_docker_image(final_tag, image_tags[-1], build_id, files)
    image_tags.append(final_tag)

    if clean_up:
        remove_partial_build_images(build_id)
        shutil.rmtree(os.path.join(PATH_BUILD, build_id))
        return [final_tag]

    return image_tags
