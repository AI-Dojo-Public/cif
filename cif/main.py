import os
import shutil
from uuid import uuid1
from docker import from_env
from argparse import ArgumentParser


PATH_BASE = os.path.dirname(__file__).rsplit("/", 1)[0]
PATH_IMAGES = os.path.join(PATH_BASE, "images")
PATH_BUILD = os.path.join(PATH_BASE, ".build")

docker_client = from_env()


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


def build_image(image_directory: str, image_tag: str, variables_override: list[str]):
    build_args: dict[str, str] = dict([variable.split("=", 1) for variable in variables_override])
    docker_client.images.build(path=image_directory, tag=image_tag, buildargs=build_args)


def image_pipeline(repository: str, build_id: str, image_name: str, previous_tag: str, variables_override: list[str], firehole_config: str) -> str:
    previous_tag_name = previous_tag.rsplit("/", 1)[1] + "_" if previous_tag else ""
    image_tag = f"{repository}{'' if repository.endswith('/') else '/'}{previous_tag_name}{image_name.replace('_', '')}"
    image_directory = copy_image(build_id, image_name, firehole_config if image_name == "firehole" else "")
    update_image(image_directory, image_name, previous_tag)
    build_image(image_directory, image_tag, variables_override)

    return image_tag


def main():
    parser = ArgumentParser()
    parser.add_argument("images", nargs="*")
    parser.add_argument("-v", "--variable", action='append')
    parser.add_argument("-fc", "--firehole-config")
    parser.add_argument("-r", "--repository", default="repository")
    required_images = parser.parse_args().images
    variables_override = parser.parse_args().variable
    firehole_config = parser.parse_args().firehole_config
    image_repository = parser.parse_args().repository

    build_id = str(uuid1())
    images: list[str] = ["_base"] + required_images
    image_tags: list[str] = list()
    for image in images:
        print(f"Building image {image}.. ")
        tag = image_pipeline(image_repository, build_id, image, image_tags[-1] if len(image_tags) > 0 else "", variables_override, firehole_config)
        image_tags.append(tag)
        print("Success.")
        print(f"Tagged as {tag}\n")
