from __future__ import annotations

import logging
import re
import subprocess
import typing

import click
import dataclasses

from . import __doc__

log = logging.getLogger(__name__)

Pods = typing.Sequence[str]
Pod = str


class KatieException(Exception):
    pass


@dataclasses.dataclass()
class Requirement:
    label: str
    operator: str
    value: str

    regex = re.compile("(?P<label>.+)(?P<operator>=|==|!=)(?P<value>.+)")

    aliases = {
        'name': 'app.kubernetes.io/name',
        'instance': 'app.kubernetes.io/instance',
        'version': 'app.kubernetes.io/version',
        'component': 'app.kubernetes.io/component',
        'part-of': 'app.kubernetes.io/part-of',
        'managed-by': 'app.kubernetes.io/managed-by',
    }

    def __str__(self) -> str:
        return f"{self.label}{self.operator}{self.value}"

    def alias(self) -> Requirement:
        return dataclasses.replace(self, label=self.aliases.get(self.label, self.label))

    @classmethod
    def from_string(cls, string: str) -> Requirement:
        match = cls.regex.match(string)

        if not match:
            raise KatieException(f"Could not parse selector {string}")

        return cls(**match.groupdict())


@dataclasses.dataclass()
class Selector:
    requirements: typing.Sequence[Requirement]

    def __str__(self) -> str:
        return ','.join(str(r) for r in self.requirements)

    def alias(self) -> Selector:
        return dataclasses.replace(self, requirements=[r.alias() for r in self.requirements])

    @classmethod
    def from_string(cls, string: str) -> Selector:
        return cls(requirements=[Requirement.from_string(s) for s in string.split(',')])


class SelectorType(click.ParamType):
    def convert(
            self,
            value: str,
            param: typing.Optional[click.Parameter],
            ctx: typing.Optional[click.Context]) -> Selector:
        return Selector.from_string(value)


@dataclasses.dataclass()
class Katie(object):
    def exec(
            self,
            selector: Selector,
            command: typing.Sequence[str],
            container: typing.Optional[str] = None) -> None:
        kubectl: typing.Sequence[str] = (
            'kubectl', 'exec', self.pod(selector), '--tty=true', '--stdin=true')

        if container:
            kubectl = (*kubectl, f'--container={container}')

        self._run((*kubectl, '--', *command))

    def logs(self, selector: Selector) -> None:
        self._run(('kubectl', 'logs', self.pod(selector)))

    def pod(self, selector: Selector) -> Pod:
        selected_pods = self.pods(selector)

        if len(selected_pods) > 1:
            log.warning("Selected multiple pods, using the first pod returned")

        return selected_pods[0]

    def pods(self, selector: Selector, enable_aliases: bool = True) -> Pods:
        aliased_selector = selector.alias()

        selected_pods = self._get_pods(selector)

        if enable_aliases and not selected_pods and selector != aliased_selector:
            log.info('Search returned no pods, attempting with aliased labels')
            selected_pods = self._get_pods(aliased_selector)

        return selected_pods

    def _get_pods(self, selector: Selector) -> Pods:
        result = self._run((
            "kubectl",
            "get",
            "pods",
            "--selector", str(selector),
            "--output", "jsonpath={.items[*].metadata.name}"),
            stdout=subprocess.PIPE)

        return result.stdout.splitlines()

    @staticmethod
    def _run(
            command: typing.Sequence[str],
            stdout: typing.Optional[int] = None,
            stderr: typing.Optional[int] = None,
    ) -> subprocess.CompletedProcess:
        log.info(f"Running '{' '.join(command)}'")
        log.debug(f"Running {command}")
        try:
            return subprocess.run(
                command,
                stdout=stdout,
                stderr=stderr,
                encoding='utf-8',
                check=True)
        except subprocess.CalledProcessError as error:
            exit(error.returncode)


@click.group(name='katie', help=__doc__)
@click.option(
    '-v', '--verbose', 'verbose',
    count=True,
    help='Increase logging detail (can be used twice).')
@click.pass_context
def main(ctx: click.Context, verbose: int):
    levels = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}
    logging.basicConfig(level=levels[verbose])

    ctx.obj = Katie()


@main.command(name='pods')
@click.argument('selector', type=SelectorType(), required=True)
@click.pass_obj
def pods(katie: Katie, selector: Selector):
    """List pods matching a selector."""
    for pod in katie.pods(selector):
        click.echo(pod)


@main.command(name='exec')
@click.option(
    '-c', '--container',
    type=click.STRING,
    required=False,
    help="Use a specific container in the pod.")
@click.argument('selector', type=SelectorType(), required=True)
@click.argument('command', type=click.STRING, required=True, nargs=-1)
@click.pass_obj
def run_command(
        katie: Katie,
        container: str,
        selector: Selector,
        command: typing.Sequence[str]) -> None:
    """Execute a command inside a pod."""
    katie.exec(selector, command, container=container)


@main.command(name='logs')
@click.argument('selector', type=SelectorType(), required=True)
@click.pass_obj
def logs(katie: Katie, selector: Selector) -> None:
    """Get logs for a pod."""
    katie.logs(selector)
