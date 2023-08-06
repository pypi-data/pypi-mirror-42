from conform.models import *
from conform.nodes import *
import logging


class BaseMapper:
    def __init__(self):
        self.named = {}

    def map_yaml(self, dict_):
        if not dict_:
            return
        for name, value in dict_.items():
            full_name = f'yaml.{name}'
            file_node = FileReaderNode(value.filename)
            yaml_node = YamlNode(file_node)
            self.named[full_name] = NamedNode(full_name, yaml_node)

    def map_http(self, dict_):
        if not dict_:
            return
        for name, value in dict_.items():
            full_name = f'http.{name}'
            http_node = HttpNode(value.url, value.method.value)
            self.named[full_name] = NamedNode(full_name, http_node)

    def map_sources(self, sources):
        if sources == None:
            return []
        for name in sources.split(','):
            if name not in self.named:
                raise ValueError(f'Unknown source {name}')
            yield self.named[name]

    def map_transform(self, dict_):
        if not dict_:
            return
        for name, config in dict_.items():
            full_name = f'transform.{name}'
            template_node = FileReaderNode(config.filename)
            sources = {
                x.name.split('.')[-1]: x
                for x in self.map_sources(config.sources)
            }
            transform_node = TransformNode(template_node, sources)
            if config.connection:
                connection_name = config.connection.split('.')[-1]
                connection = self.document.connection[connection_name]
                file_node = RemoteFileNode(config.destination, transform_node,
                                           connection)
            else:
                file_node = LocalFileNode(config.destination, transform_node)
            yield NamedNode(full_name, file_node)

    def map_document(self, document: Document):
        self.document = document
        self.map_yaml(document.yaml)
        self.map_http(document.http)
        return RootNode(list(self.map_transform(document.transform)))
