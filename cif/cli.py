from argparse import ArgumentParser
from itertools import cycle
from pprint import pp
from threading import Thread, Event
from time import sleep

from cif.builder import build
from cif.helpers import available_services, available_actions, FileCopy


def parse_image_variables(variables_raw: list[str]) -> dict[str, str]:
    return dict(variable.split("=", 1) for variable in variables_raw)


def parse_actions(action_definitions: list[str]) -> list[tuple[str, dict[str, str]]]:
    parsed_actions: list[tuple[str, dict[str, str]]] = list()
    for action in action_definitions:
        action_name, action_variables_raw = action.split(":", 1)
        action_variables = dict(variable.split("=", 1) for variable in action_variables_raw.split(","))
        parsed_actions.append((action_name, action_variables))

    return parsed_actions


def loading(stopped: Event):
    animation_frames = [
        [
            " /^v^\\",
            "           \\^v^/",
        ],
        [
            " \\^v^/",
            "           /^v^\\",
        ],
        [
            " /^v^\\",
            "           \\^v^/",
        ],
        [
            "            \\^v^/",
            "  /^v^\\",
        ],
        [
            "            /^v^\\",
            "  \\^v^/",
        ],
    ]
    num_of_frames = len(animation_frames[0])
    longest_frame = max([len(f) for fs in animation_frames for f in fs])
    for frames in cycle(animation_frames):
        if stopped.is_set():
            break
        for frame in frames:
            print(f"{frame}{' ' * (longest_frame-len(frame))}\n", end="")
        sleep(0.3)
        print("\033[F" * num_of_frames, end="")


def parse_files(raw_files: list[str]) -> list[FileCopy]:
    files: list[FileCopy] = list()
    for file in raw_files:
        match file.split(":", 4):
            case [host_path, image_path]:
                files.append((host_path, image_path, None, None, None))
            case [host_path, image_path, user, group, mode]:
                files.append(
                    (host_path, image_path, user if user else None, group if group else None, mode if mode else None)
                )
            case _:
                raise ValueError(
                    f"File is not correctly defined: {file}\n"
                    f"You need `/host/path:/image/path:username:groupname:mode` or `/host/path:/image/path`"
                )

    return files


def main():
    parser = ArgumentParser(description="Forge multiple services into a single image.")
    parser.add_argument("tag", help="Tag the image - just like in Docker.")
    parser.add_argument("-s", "--service", action="append", default=list(), help="Service to use.")
    parser.add_argument(
        "-v", "--variable", action="append", default=list(), help="Variable for the image. (MY_VAR=var)"
    )
    parser.add_argument(
        "-a",
        "--action",
        action="append",
        default=list(),
        help="Action with variables. (create-user:USER_NAME=user,USER_PASSWORD=user)",
    )
    parser.add_argument("-ls", "--list-services", action="store_true", help="Show possible services.")
    parser.add_argument("-la", "--list-actions", action="store_true", help="Show possible actions.")
    parser.add_argument("-p", "--package", action="append", default=list(), help="System package to install.")
    parser.add_argument(
        "-f",
        "--file",
        action="append",
        default=list(),
        help="Add file to the image (/host/path:/image/path:username:groupname:mode). "
        "To leave out the parameter, simply skip it (e.g. /file.txt:/file.txt:::440).",
    )
    parser.add_argument(
        "-k", "--keep-images", action="store_true", help="Keep artifacts from the build (tmp images, tmp files)."
    )
    list_services: bool = parser.parse_args().list_services
    list_actions: bool = parser.parse_args().list_actions
    services: list[str] | str = parser.parse_args().service
    variables: list[str] | str = parser.parse_args().variable
    actions: list[str] | str = parser.parse_args().action
    image_tag: str = parser.parse_args().tag
    packages: list[str] | str = parser.parse_args().package
    clean_up: bool = not parser.parse_args().keep_images
    files: list[str] | str = parser.parse_args().file

    if list_services:
        pp(available_services())
        return

    if list_actions:
        pp(available_actions())
        return

    parsed_files = parse_files(files)
    parsed_image_variables = parse_image_variables(variables)
    parsed_actions = parse_actions(actions)

    stop_loading = Event()
    loading_thread = Thread(target=loading, args=(stop_loading,), daemon=True)
    loading_thread.start()

    try:
        tags = build(
            services,
            parsed_image_variables,
            parsed_actions,
            image_tag,
            packages,
            parsed_files,
            clean_up,
        )
    except ValueError as ex:
        print(str(ex))
    else:
        print(f"Created tags:\n{chr(10).join(tags)}")
    finally:
        stop_loading.set()
