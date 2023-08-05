import asyncio
import subprocess
from collections import defaultdict

from .logger import log


class HomeBrew:
    __slots__ = ("_installed", "_uses")

    def __init__(self):
        self._installed = self._get_installed()
        self._uses = {}
        self._get_uses()

    def _get_installed(self):
        result = subprocess.check_output(["brew", "list"])
        installed = result.split()
        return [r.decode() for r in installed]

    def _get_uses(self):
        tasks = [self._get_uses_for_package(package) for package in self._installed]
        asyncio.run(asyncio.wait(tasks))

    async def _get_uses_for_package(self, package):
        uses = await asyncio.create_subprocess_shell(
            f"brew uses --installed {package}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        stdout, _ = await uses.communicate()
        self._uses[package] = stdout.decode().split()

    @property
    def installed_packages(self):
        return self._installed

    @property
    def packages_not_needed_by_other(self):
        return {key: val for key, val in self._uses.items() if not val}

    @property
    def packages_needed_by_other(self):
        return {key: val for key, val in self._uses.items() if val}

    @property
    def package_dependencies(self):
        dependencies = defaultdict(list)
        for package, needed_by in self.packages_needed_by_other.items():
            for needed in needed_by:
                dependencies[needed].append(package)
        return {needed: sorted(packages) for needed, packages in dependencies.items()}

    @property
    def info(self):
        log(
            self.installed_packages,
            self.packages_not_needed_by_other,
            self.packages_needed_by_other,
            self.package_dependencies,
        )
