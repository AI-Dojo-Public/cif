import os
import shutil
from uuid import uuid1
from docker import from_env


PATH_BASE = os.path.dirname(__file__).rsplit("/", 1)[0]
PATH_IMAGES = os.path.join(PATH_BASE, "images")
PATH_BUILD = os.path.join(PATH_BASE, ".build")
GITLAB_REPOSITORY = "repository/"

docker_client = from_env()


def copy_image(build_id: str, image_name: str) -> str:
    image_directory: str = os.path.join(PATH_IMAGES, image_name)
    tmp_image_directory: str = os.path.join(PATH_BUILD, build_id, image_name)
    shutil.copytree(image_directory, tmp_image_directory)

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


def build_image(image_directory: str, image_tag: str) -> str:
    docker_client.images.build(path=image_directory, tag=image_tag)


def image_pipeline(build_id: str, image_name: str, previous_tag: str) -> str:
    image_tag = f"{GITLAB_REPOSITORY}{image_name}".replace("_", "")
    image_directory = copy_image(build_id, image_name)
    update_image(image_directory, image_name, previous_tag)
    build_image(image_directory, image_tag)

    return image_tag


def main(required_images: list[str]):
    build_id = str(uuid1())
    images: list[str] = ["_base"] + required_images
    image_tags: list[str] = list()
    for image in images:
        tag = image_pipeline(build_id, image, image_tags[-1] if len(image_tags) > 0 else "")
        image_tags.append(tag)


if __name__ == '__main__':
    main(["ssh"])
