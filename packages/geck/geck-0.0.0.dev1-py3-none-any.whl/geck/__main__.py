import os
import subprocess
import tempfile

from .cli import parser


def run():
    print('Starting')
    #d = tempfile.TemporaryDirectory(prefix='geck_')
    #tempdir = d.name
    tempdir = '/tmp/meta_geck/'
    print(f'made {tempdir}')
    print('making virtualenv...')
    output = subprocess.run(
        [
            'python3',
            '-m',
            'venv',
            os.path.join(tempdir, 'env'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print('Done')
    print('Installing...', )
    output = subprocess.run(
        [
            os.path.join(tempdir, 'env', 'bin', 'python'),
            '-m',
            'pip',
            'install',
            '-e',
            '/home/wayne/programming/geck',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print('Done')
    print('Installing test_requirements...', )
    output = subprocess.run(
        [
            os.path.join(tempdir, 'env', 'bin', 'python'),
            '-m',
            'pip',
            'install',
            'geck[testing,building]',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(output.stdout.decode())
    print(output.stderr.decode())
    print('Done')
    print('running tests')
    output = subprocess.run(
        [
            os.path.join(tempdir, 'env', 'bin', 'pytest'),
            'tests',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if output.returncode != 0:
        print('Tests failed')
    else:
        print('Tests passed')
    print('building wheel')
    output = subprocess.run(
        [
            os.path.join(tempdir, 'env', 'bin', 'python'),
            'setup.py',
            'bdist_wheel',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print('wheel built')
    print(output.stdout.decode())
    print('*'*30)
    print(output.stderr.decode())

    output = subprocess.run(
        [
            os.path.join(tempdir, 'env', 'bin', 'pip'),
            'show',
            'geck',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    version_string = [line for line in output.stdout.decode().split('\n')
                      if line.startswith('Version: ')]
    version = version_string[0].split()[1]
    print(f'Version: {version!r}')
    print('Tagging version in git')
    output = subprocess.run([
        'git',
        'tag',
        version,
    ])
    print('Done')
    print('Pushing tags')
    output = subprocess.run([
        'git',
        'push',
        '--tags',
    ])
    print('done')



if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
