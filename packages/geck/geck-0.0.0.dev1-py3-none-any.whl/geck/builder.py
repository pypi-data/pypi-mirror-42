import runpy

from pathlib import Path

# TODO: This should come from geck config/data dir -W. Werner, 2019-02-26
LAST_ID = 0


class Build:
    def __init__(self, root='.'):
        self.id = LAST_ID + 1
        self.root = Path(root.format(self.__dict__)).expanduser().absolute()

    def run(self):
        print(f'I can run in {self.root}!')


def run(filename):
    job = runpy.run_path(filename)
    job['build'].run()


def build(args):
    '''
    Take a ``Namespace``-like object and if `.action` is queue,
    queue up the build, or if it is 'run', run the build right now.
    '''
    if args.action == 'queue':
        raise NotImplemented('Pull requests welcome! This feature does not yet exist')
    elif args.action == 'run':
        run(args.script)
    else:
        raise NotImplemented(f'Unknown action {args.action}')
