import signal
import sys

signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(1))

import argparse
import gettext
import os
import pexpect
import pkg_resources
import re
import shlex
import shutil
import subprocess

import inflect

from . import __version__

# Internationalization
t = gettext.translation("cli50", pkg_resources.resource_filename("cli50", "locale"), fallback=True)
t.install()

def main():

    # Listen for ctrl-c
    signal.signal(signal.SIGINT, handler)

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fast", action="store_true", help=_("skip autoupdate"))
    parser.add_argument("-l", "--login", const=True, default=False, help=_("log into container"),
                        metavar="CONTAINER", nargs="?")
    parser.add_argument("-d", "--dotfile", action="append", default=[],
                        help=_("dotfile in your $HOME to mount read-only in container's $HOME"), metavar="DOTFILE")
    parser.add_argument("-S", "--stop", action="store_true", help=_("stop any containers"))
    parser.add_argument("-t", "--tag", help=_("start cs50/cli:TAG, else cs50/cli:latest"), metavar="TAG")
    parser.add_argument("-V", "--version", action="version",
                        version="%(prog)s {}".format(__version__))
    parser.add_argument("directory", default=os.getcwd(), metavar="DIRECTORY",
                        nargs="?", help=_("directory to mount, else $PWD"))
    args = vars(parser.parse_args())

    # Check for Docker
    if not shutil.which("docker"):
        parser.error(_("Docker not installed."))

    # Image to use
    image = f"cs50/cli:{args['tag']}" if args["tag"] else "cs50/cli"

    # Stop containers
    if args["stop"]:
        try:
            stdout = subprocess.check_output([
                "docker", "ps",
                "--all",
                "--format", "{{.ID}}\t{{.Image}}"
            ]).decode("utf-8")
            for line in stdout.rstrip().splitlines():
                ID, Image = line.split("\t")
                if Image == image:
                    subprocess.check_call(["docker", "stop", "--time", "0", ID])
            sys.exit(0)
        except subprocess.CalledProcessError:
            sys.exit(1)

    # Ensure directory exists
    directory = os.path.realpath(args["directory"])
    if not os.path.isdir(directory):
        parser.error(_("{}: no such directory").format(args['directory']))

    # Log into container
    if args["login"]:

        # If container specified
        if isinstance(args["login"], str):
            try:
                print(ports(args["login"]))
                login(args["login"])
            except:
                sys.exit(1)
            else:
                sys.exit(0)

        # Check for running containers
        try:
            stdout = subprocess.check_output([
                "docker", "ps",
                "--all",
                "--filter", "status=running",
                "--format", "{{.ID}}\t{{.Image}}\t{{.RunningFor}}\t{{.Mounts}}",
                "--no-trunc"
            ]).decode("utf-8")
        except subprocess.CalledProcessError:
            sys.exit(1)
        else:
            containers = []
            for line in stdout.rstrip().splitlines():
                ID, Image, RunningFor, *Mounts = line.split("\t")
                Mounts = Mounts[0].split(",") if Mounts else []
                Mounts = [Mount for Mount in Mounts if not re.match(r"^[0-9a-fA-F]{64}$", Mount)]  # Ignore hashes
                containers.append((ID, Image, RunningFor.lower(), Mounts))
        if not containers:
            sys.exit("No containers are running.")

        # Ask whether to use a running container
        for ID, Image, RunningFor, Mounts in containers:
            while True:
                prompt = _("Log into {}, started {}").format(Image, RunningFor)
                if Mounts:
                    prompt += _(" with {} mounted").format(inflect.engine().join(Mounts))
                prompt += "? [Y] "
                stdin = input(prompt)
                if re.match("^\s*(?:y|yes)?\s*$", stdin, re.I):
                    try:
                        print(ports(ID))
                        login(ID)
                    except:
                        sys.exit(1)
                    else:
                        sys.exit(0)
                else:
                    break
        else:
            sys.exit(0)

    # Pull image if not found locally, autoupdate unless skipped
    try:
        subprocess.check_call(["docker", "image", "inspect", image], stdout=subprocess.DEVNULL)
        assert args["fast"]
    except (AssertionError, subprocess.CalledProcessError):
        try:
            subprocess.check_call(["docker", "pull", image])
        except subprocess.CalledProcessError:
            sys.exit(1)

    # Options
    options = ["--interactive",
               "--publish-all",
               "--rm",
               "--security-opt", "seccomp=unconfined",  # https://stackoverflow.com/q/35860527#comment62818827_35860527
               "--tty",
               "--volume", directory + ":/home/ubuntu/workspace",
               "--workdir", "/home/ubuntu/workspace"]

    # Mount each dotfile in user's $HOME read-only in container's $HOME
    for dotfile in args["dotfile"]:
        home = os.path.join(os.path.expanduser("~"), "")
        if dotfile.startswith("/") and not dotfile.startswith(home):
            sys.exit(_("{}: not in your $HOME").format(dotfile))
        elif dotfile.startswith(os.path.join("~", "")):
            dotfile = os.path.expanduser(dotfile)
        else:
            dotfile = os.path.join(home, dotfile)
        if not os.path.exists(dotfile):
            sys.exit(_("{}: No such file or directory").format(dotfile))
        if not dotfile[len(home):].startswith("."):
            sys.exit(_("{}: Not a dotfile").format(dotfile))
        options += ["--volume", "{}:/home/ubuntu/{}:ro".format(dotfile, dotfile[len(home):])]

    # Mount directory in new container
    try:

        # Create container
        columns, lines = shutil.get_terminal_size()  # Temporary
        options += [ # Temporary
            "--env", f"COLUMNS={str(columns)},LINES={str(lines)}",
            "--env", f"LINES={str(lines)}"]
        container = subprocess.check_output(["docker", "create"] + options + [image, "bash", "--login"]).decode("utf-8").rstrip()

        # Start container
        child = pexpect.spawn("docker", ["start", "--attach", "--interactive", container], dimensions=(lines, columns),
                              env=dict(os.environ, COLUMNS=str(columns), LINES=str(lines)))  # Temporary

        # Once running, list port mappings
        child.expect(".*\$")
        print(ports(container))

        # Let user interact with container
        print(child.after.decode("utf-8"), end="")
        child.interact()

    except (pexpect.exceptions.ExceptionPexpect, subprocess.CalledProcessError):
        sys.exit(1)
    else:
        sys.exit(0)


def handler(number, frame):
    """Handle SIGINT."""
    print()
    sys.exit(0)


def login(container):
    """Log into container."""
    columns, lines = shutil.get_terminal_size()  # Temporary
    try:
        subprocess.check_call([
            "docker", "exec",
            "--env", f"COLUMNS={str(columns)},LINES={str(lines)}",  # Temporary
            "--env", f"LINES={str(lines)}",  # Temporary
            "--interactive",
            "--tty",
            container,
            "bash",
            "--login"
        ])
    except subprocess.CalledProcessError:
        raise RuntimeError() from None


def ports(container):
    """Return port mappings for container."""
    return subprocess.check_output([
        "docker", "ps",
        "--filter", f"id={container}",
        "--format", "{{.Ports}}",
        "--no-trunc"
    ]).decode("utf-8").rstrip()


if __name__ == "__main__":
    main()
