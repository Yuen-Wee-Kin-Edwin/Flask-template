import os


def running_in_docker():
    """
    Check if the application is running inside a Docker container
    by checking for the presence of /.dockerenv.
    """
    return os.path.exists("/.dockerenv")
