'''
GECK self-build script.
'''
import geck

build = geck.builder.Build(
    root='~/build/metageck',
)
build.add_step(
)

if __name__ == '__main__':
    import sys
    print(f'No - run this with GECK. geck builder {__file__} run', file=sys.stderr)
    sys.exit(1)
