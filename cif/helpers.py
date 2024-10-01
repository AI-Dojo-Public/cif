from os import listdir
from os.path import join, isdir

from cif.settings import PATH_SERVICES, PATH_ACTIONS


def parse_dockerfile_variables(dockerfile_path: str):
    with open(join(dockerfile_path, "Dockerfile")) as dockerfile:
        environment: dict[str, str] = dict()
        build_arguments: dict[str, str] = dict()
        for line in dockerfile.readlines():
            if line.startswith("ARG"):
                argument_name, argument_value = line.removeprefix("ARG ").removesuffix("\n").split("=", 1)
                build_arguments[argument_name] = argument_value
            if line.startswith("ENV"):
                variable_name, variable_value = line.removeprefix("ENV ").removesuffix("\n").split("=", 1)
                environment[variable_name] = variable_value

    return build_arguments, environment


def available_services() -> list[tuple[str, dict[str, str], dict[str, str]]]:
    """
    Get available services and their variables.
    :return: Service name, build arguments, and environment variables
    """
    response: list[tuple[str, dict[str, str], dict[str, str]]] = list()
    for directory in [file for file in listdir(PATH_SERVICES) if isdir(join(PATH_SERVICES, file))]:
        build_arguments, environment = parse_dockerfile_variables(join(PATH_SERVICES, directory))
        response.append((directory, build_arguments, environment))

    return response


def available_actions() -> list[tuple[str, dict[str, str], dict[str, str]]]:
    """
    Get available services and their variables.
    :return: Service name, build arguments, and environment variables
    """
    response: list[tuple[str, dict[str, str], dict[str, str]]] = list()
    for directory in [file for file in listdir(PATH_ACTIONS) if isdir(join(PATH_ACTIONS, file))]:
        build_arguments, environment = parse_dockerfile_variables(join(PATH_ACTIONS, directory))
        response.append((directory, build_arguments, environment))

    return response


def check_for_forbidden_services(services: list[str]):
    desired_services = set(services)

    allowed_services = set([file for file in listdir(PATH_SERVICES) if isdir(join(PATH_SERVICES, file))])
    allowed_services.difference_update([service for service in allowed_services if service.startswith("_")])

    return desired_services.difference(allowed_services)
