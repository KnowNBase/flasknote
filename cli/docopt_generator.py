import typing as t

# noinspection Mypy
from docopt import docopt

from cli.generator import Chain


class Generator:
    def __call__(self, links: t.List[Chain]) -> t.Dict[str, t.Callable]:
        commands = {}
        for link in links:
            command = create_command(link)
            command_name = link.command_name
            commands[command_name] = command
        return commands


def create_command(link: Chain) -> t.Callable:
    def command(args):
        # print(f"||| run command {link.command_name} with:")
        # print(f"||| args: {args}")
        args = docopt(link.command_doc, argv=args)
        UseCase = link.usecase
        uc = UseCase(**link.dependencies)
        input_ = link.parse_input(args)
        output = uc(input_)
        link.present_output(output)

    return command
