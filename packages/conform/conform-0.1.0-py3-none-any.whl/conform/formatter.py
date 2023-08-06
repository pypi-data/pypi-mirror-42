from colorama import init
init()

import asyncio
from conform.nodes import NamedNode
from colorama import Fore, Back, Style, Cursor

import warnings
warnings.filterwarnings("ignore")


class Formatter():
    def __init__(self, nodes):
        self.nodes = nodes

    async def execute(self, terminal_width=50):
        named_nodes = [x for x in self.nodes if isinstance(x, NamedNode)]
        max_name_width = max(len(x.name) for x in named_nodes)
        while True:
            for node in named_nodes:
                if node.progress == 1:
                    completed = False
                if node.progress == 0:
                    color = Style.DIM + Fore.BLUE
                elif node.progress == 1:
                    color = Fore.GREEN
                else:
                    color = Fore.WHITE
                spacing = ' ' * (max_name_width - len(node.name))
                progress_text = "=" * (
                    terminal_width - max_name_width - 6) * node.progress
                line = f'→ {color}{node.name} {spacing}[{progress_text}>]{Style.RESET_ALL}'
                print(line)

            await asyncio.sleep(0.1)
            completed = all([x.progress == 1 for x in named_nodes])
            if completed:
                break
            print(Cursor.UP(len(named_nodes)), end='')


class ErrorFormatter:
    def format_header(self, message, width=80):
        return Style.DIM + Fore.BLUE + '-- ' + message + ' ' + '-' * (
            width - len(message) - 4) + Style.RESET_ALL


class ValidationErrorCliFormatter(ErrorFormatter):
    def format(self, validation_error):
        output = []
        output.append(self.format_header('Validation Error'))
        for error in validation_error.errors():
            output.append(Fore.RED + '--' + '.'.join(error['loc']) +
                          Style.RESET_ALL)
            output.append(f'  {error["msg"]} ({error["type"]})')
        return '\n'.join(output)
