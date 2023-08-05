import argparse

from openapi_toolkit import OpenAPI, yaml


def app(argv=None):
    parser = argparse.ArgumentParser(description='OpenAPI Toolkit CLI')
    subparsers = parser.add_subparsers(dest='command')

    resolve_parser = subparsers.add_parser('resolve', description='Resolve OpenAPI Spec')
    resolve_parser.add_argument('filename', type=str, help='Path of spec to resolve.')
    resolve_parser.add_argument(
        '--preprocessor',
        type=str,
        choices=['mako'],
        help=(
            'Enable a preprocessor to use on the specification. '
            'Requires openapi-toolkit[\'preprocessor\'].'
        )
    )
    resolve_parser.add_argument(
        '--save-path',
        type=str,
        help='Path to save resolved content.'
    )

    args = parser.parse_args()

    if args.command == 'resolve':

        preprocessor = None
        if args.preprocessor:
            # Import here to avoid requiring the dep all the time
            from openapi_toolkit.preprocessor import MakoPreprocessor
            preprocessor = MakoPreprocessor()

        spec = OpenAPI.load(args.filename, preprocessor=preprocessor)

        if args.save_path:
            spec.save(args.save_path)
        else:
            print(yaml.dump(spec.specification))

    else:
        parser.print_help()
