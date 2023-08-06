import aiofiles
import aiohttp
import asyncio
import jinja2
import toml
import yaml
import paramiko
import logging
from pathlib import Path
from paramiko.client import SSHClient
from concurrent.futures import ThreadPoolExecutor

#logging.basicConfig(level=logging.DEBUG)


class BaseNode:
    def __init__(self):
        self.future = None
        self.progress = 0

    def set_future(self, future):
        self.future = future

    async def execute(self):
        self.progress = 0
        logging.debug(f'excuting {self} started')
        value = await self.resolve()
        logging.debug(f'excuting {self} finished')
        self.progress = 1
        self.future.set_result(value)

    async def unwrap(self):
        return await self.future

    async def resolve(self):
        raise NotImplemented()

    def __str__(self):
        return f'- {self.__class__.__name__}'


class FileReaderNode(BaseNode):
    def __init__(self, filename):
        self.filename = filename

    async def resolve(self):
        async with aiofiles.open(self.filename, mode='r') as file:
            return await file.read()

    def __str__(self):
        return f'- FileReaderNode filename={self.filename}'


class YamlNode(BaseNode):
    def __init__(self, file):
        self.file = file

    @property
    def edges(self):
        return [self.file]

    async def resolve(self):
        return yaml.load(await self.file.unwrap())


class HttpNode(BaseNode):
    def __init__(self, url, method):
        self.url = url
        self.method = method

    async def resolve(self):
        async with aiohttp.ClientSession() as session:
            async with session.request(self.method, self.url) as response:
                if response.content_type == 'application/json':
                    return await response.json()
                else:
                    raise ValueError(
                        f'Unsupported content_type {response.content_type}')


class SourcesNode(BaseNode):
    def __init__(self, sources):
        self.sources = sources

    @property
    def edges(self):
        return self.sources

    async def resolve(self):
        return await asyncio.gather(self.sources)


class TransformNode(BaseNode):
    def __init__(self, template, sources):
        self.template = template
        self.sources = sources

    @property
    def edges(self):
        return [self.template] + list(self.sources.values())

    async def resolve(self):
        context = {}
        for name, source in self.sources.items():
            context[name] = await source.unwrap()
        template = jinja2.Template(await self.template.unwrap())
        return template.render(**context)


class LocalFileNode(BaseNode):
    def __init__(self, filename, transform):
        self.filename = filename
        self.transform = transform

    @property
    def edges(self):
        return [self.transform]

    async def resolve(self):
        contents = await self.transform.unwrap()
        Path(self.filename).parent.mkdir(
            parents=True, 
            exist_ok=True)
        async with aiofiles.open(self.filename, mode='w') as file:
            return await file.write(contents)

    def __str__(self):
        return f'- LocalFileNode filename={self.filename}'


class RemoteFileNode(BaseNode):
    def __init__(self, filename, transform, connection):
        self.filename = filename
        self.transform = transform
        self.connection = connection

    @property
    def edges(self):
        return [self.transform]

    async def resolve(self):
        contents = await self.transform.unwrap()
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            result = loop.run_in_executor(pool, self.write_file_contents,
                                          contents)
            return await result

    def write_file_contents(self, contents):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=self.connection.hostname,
            username=self.connection.username,
            key_filename=self.connection.private_key)

        sftp = client.open_sftp()
        with sftp.open(self.filename, 'w') as file:
            file.write(contents)


class NamedNode(BaseNode):
    def __init__(self, name, target):
        self.name = name
        self.target = target

    @property
    def edges(self):
        return [self.target]

    async def resolve(self):
        return await self.target.unwrap()

    def __str__(self):
        return f'- NamedNode name={self.name}'


class RootNode(BaseNode):
    def __init__(self, children):
        self.children = children

    @property
    def edges(self):
        return self.children

    def resolve(self):
        return asyncio.gather(*[x.unwrap() for x in self.children])
