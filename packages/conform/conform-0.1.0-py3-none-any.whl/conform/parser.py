import re


class ArgDictParser():
    def parse(self, args):
        dict_ = {}
        for arg in args:
            match = re.match(r'--([\w.]+)+=(.+)', arg)
            if not match:
                raise ValueError(f'Unknown argument "{arg}"')
            self.populate_dict(dict_, match.group(1), match.group(2))
        return dict_

    def populate_dict(self, dict_, path, value):
        split = path.split('.')
        context = dict_
        for part in split[:-1]:
            if part not in context:
                context[part] = {}
            context = context[part]
        context[split[-1]] = value
