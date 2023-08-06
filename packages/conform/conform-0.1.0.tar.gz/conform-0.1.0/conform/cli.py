import click
import toml
import asyncio
import logging
from pydantic import ValidationError
from graphviz import Digraph
from conform.models import Document
from conform.mapping import BaseMapper
from conform.parser import ArgDictParser
from conform.formatter import Formatter, ValidationErrorCliFormatter

def map_to_nodes(filename, args):
    if filename: 
        with open(filename) as file:
            contents = toml.load(file)
    else:
        parser = ArgDictParser()
        contents = parser.parse(args)

    try:
        document = Document.parse_obj(contents)
    except ValidationError as error:
        formatter = ValidationErrorCliFormatter()
        click.echo(formatter.format(error), err=True)
        raise click.Abort()

    mapper = BaseMapper()
    return mapper.map_document(document)

def get_all_nodes(node):
    list_ = []
    visit_node(list_, node)
    return list_

def visit_node(list_, node):
    if hasattr(node, 'permanent'):
        return
    if hasattr(node, 'temporary'):
        raise ValueError('Not a DAG')
    setattr(node, 'temporary', True)
    if hasattr(node, 'edges'):
        for edge in node.edges:
            logging.debug(node)
            visit_node(list_, edge)
    setattr(node, 'permanent', True)
    list_.append(node)

def visit_node_graph(graph, node):
    graph.node(str(id(node)), str(node))
    if not hasattr(node, 'edges'):
        return
    for edge in node.edges:
        graph.edge(str(id(edge)), str(id(node)))
        visit_node_graph(graph, edge)

@click.group()
def cli():
    pass

@cli.command()
def test():
    click.echo('Hello world!')

async def test(root_node):
    logging.debug('Started!')
    loop = asyncio.get_running_loop()
    nodes = get_all_nodes(root_node)
    logging.debug('Gathered nodes!')
    for node in nodes:
        future = loop.create_future()
        logging.debug(f'Setting future {node}!')
        node.set_future(future)
    coros = [x.execute() for x in nodes]
    formatter = Formatter(nodes)
    coros.append(formatter.execute())
    await asyncio.gather(*coros)
    logging.debug('Finished!')

@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.option('--filename')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def run(filename, args):
    root_node = map_to_nodes(filename, args)
    asyncio.run(test(root_node))

@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.option('--filename')
@click.option('--png', help='filename to output as png.')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def plan(filename, png, args):
    root_node = map_to_nodes(filename, args)
    graph = Digraph(format='png')
    visit_node_graph(graph, root_node)
    if png:
        graph.render(png)
    else:
        click.echo(graph.source)


if __name__ == '__main__':
    cli()
