#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
msbackup -- Generic archive utility.

@author:     Aleksei Badiaev <aleksei.badyaev@gmail.com>
@copyright:  2015 Aleksei Badiaev. All rights reserved.
"""

import argparse
import os
import sys

import configparser

from msbackup.backend import BACKENDS
from msbackup.archive import ARCHIVERS
from msbackup.encrypt import ENCRYPTORS
from msbackup.engine import Engine


__all__ = ('main', )
__date__ = '2015-10-08'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

UPDATE_DATE = __date__
with open(os.path.join(PROJECT_ROOT, 'UPDATE_DATE')) as update_date_file:
    UPDATE_DATE = update_date_file.read().rstrip()
__updated__ = UPDATE_DATE

VERSION = 'UNKNOWN'
with open(os.path.join(PROJECT_ROOT, 'VERSION')) as version_file:
    VERSION = version_file.read().rstrip()
__version__ = VERSION


def main(argv=None):
    """
    Entry point in application.

    :param argv: Command line arguments.
    :type argv: list
    :return: Exit code of application.
    :rtype: int
    """
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
    program_name = os.path.basename(sys.argv[0])
    program_version = 'v%s' % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version,
                                                     program_build_date)
    program_shortdesc = __import__('msbackup').msbackup.__doc__.split('\n')[1]
    program_license = """%s

  Created by Aleksei Badiaev on %s.
  Copyright 2015 Aleksei Badiaev. All rights reserved.

  Distributed on an 'AS IS' basis without warranties
  or conditions of any kind, either express or implied.

USAGE
""" % (program_shortdesc, str(__date__))

    try:
        backends = sorted([item for item in BACKENDS])
        archivers = sorted([item for item in ARCHIVERS])
        encryptors = sorted([item for item in ENCRYPTORS])
        # Setup argument parser
        parser = argparse.ArgumentParser(
            prog=program_name,
            description=program_license,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            '-c', '--config', dest='config',
            help='Path to config file.',
        )
        parser.add_argument(
            '-e', '--backend', dest='backend',
            required=True, choices=backends,
            help='Backend to make archive.',
        )
        parser.add_argument(
            '-s', '--source', dest='source',
            help='Path to source directory.',
        )
        parser.add_argument(
            '-b', '--archive-dir', dest='backup_dir',
            help='Path to archive directory (current by default).',
        )
        parser.add_argument(
            '-a', '--archiver', dest='archiver', choices=archivers,
            help='Name of file archiver.',
        )
        parser.add_argument(
            '-E', '--encryptor', dest='encryptor',
            choices=encryptors, default=None,
            help='Name of file encryptor.',
        )
        parser.add_argument(
            '-x', '--exclude', action='append',
            dest='exclude', metavar='PATTERN',
            help='Exclude files defined by the PATTERN.',
        )
        parser.add_argument(
            '-X', '--exclude-from', action='append',
            dest='exclude_from', metavar='FILE',
            help='Exclude files defined in FILE.',
        )
        parser.add_argument(
            '-r', '--rotated', dest='rotated', action='store_true',
            help='Perform rotated archive.',
        )
        parser.add_argument(
            '-v', '--verbose', dest='verbose', action='store_true',
            help='Verbose output.',
        )
        parser.add_argument(
            '-V', '--version', action='version',
            version=program_version_message,
        )
        # Process arguments
        params = parser.parse_args()
        config = configparser.RawConfigParser()
        if params.config is not None:
            config_file_path = params.config
            config.read(config_file_path)
            setattr(config, 'config_file_path', config_file_path)
        engine_kwargs = {
            'backend': params.backend,
            'config': config,
            'archiver': params.archiver,
            'encryptor': params.encryptor,
            'out': sys.stdout,
            'err': sys.stderr,
        }
        if params.exclude is not None:
            engine_kwargs['exclude'] = params.exclude
        if params.exclude_from is not None:
            engine_kwargs['exclude_from'] = params.exclude_from
        # Prepare back-end.
        engine = Engine(**engine_kwargs)
        # Perform archive.
        archive_kwargs = {
            'source': params.source,
            'backup_dir': params.backup_dir,
            'verbose': params.verbose,
        }
        if params.rotated is True:
            archive_dir = engine.rotated(**archive_kwargs)
        else:
            archive_dir = engine.backup(**archive_kwargs)
        if params.verbose:
            sys.stdout.write(u'Archive directory: {}\n'.format(archive_dir))
        return 0
    except KeyboardInterrupt:  # pragma: no coverage
        return 0
    except Exception as e:
        indent = len(program_name) * ' '
        sys.stderr.write(program_name + ': ' + repr(e) + '\n')
        sys.stderr.write(indent + '  for help use --help\n')
        return 1


if __name__ == "__main__":  # pragma: no coverage
    sys.exit(main())
