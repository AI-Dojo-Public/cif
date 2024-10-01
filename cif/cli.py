from argparse import ArgumentParser
from itertools import cycle
from pprint import pp
from threading import Thread, Event
from time import sleep

from cif.builder import build
from cif.helpers import available_services, available_actions


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


def main():
    parser = ArgumentParser()
    parser.add_argument("services", nargs="*")
    parser.add_argument(
        "-v", "--variable", action="append", default=list(), help="Variable for the image. (MY_VAR=var)"
    )
    parser.add_argument("-fc", "--firehole-config", help="Config for Firehole, otherwise it won't run.")
    parser.add_argument("-r", "--repository", default="cif", help="Docker image repository (image prefix).")
    parser.add_argument(
        "-a",
        "--action",
        action="append",
        default=list(),
        help="Action with variables. (create-user:USER_NAME=user,USER_PASSWORD=user)",
    )
    parser.add_argument('-ls', '--list-services', action='store_true', help="Show possible services.")
    parser.add_argument('-la', '--list-actions', action='store_true', help="Show possible actions.")
    list_services = parser.parse_args().list_services
    list_actions = parser.parse_args().list_actions
    services = parser.parse_args().services
    variables = parser.parse_args().variable
    actions = parser.parse_args().action
    firehole_config = parser.parse_args().firehole_config
    image_repository = parser.parse_args().repository

    if list_services:
        pp(available_services())
        return

    if list_actions:
        pp(available_actions())
        return

    parsed_image_variables = parse_image_variables(variables)
    parsed_actions = parse_actions(actions)

    stop_loading = Event()
    loading_thread = Thread(target=loading, args=(stop_loading,), daemon=True)
    loading_thread.start()

    try:
        tags = build(image_repository, services, parsed_image_variables, parsed_actions, firehole_config)
    except ValueError as ex:
        print(str(ex))
    else:
        print(f"All created tags: {' '.join(tags)}")
        print(f"Final tag: {tags[-1]}")
    finally:
        stop_loading.set()
