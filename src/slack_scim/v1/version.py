import pkg_resources  # part of setuptools


def load_package_version():
    package = pkg_resources.require("slack_scim")
    if package and len(package) > 0:
        return package[0].version or "0.0.0"


__version__ = load_package_version()
