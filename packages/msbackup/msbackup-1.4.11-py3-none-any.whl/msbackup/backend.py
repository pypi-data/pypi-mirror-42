# -*- coding: utf-8 -*-
"""Backends for 'msbackup' package."""

import os
import shutil
import subprocess
import sys
import tempfile
import abc

from msbackup import utils, archive, encrypt


class Base(metaclass=abc.ABCMeta):
    """Базовый класс архиваторов."""

    SECTION = 'DEFAULT'

    def __init__(self, config, archiver=None, encryptor=None,
                 out=None, err=None, **kwargs):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param archiver: Имя архиватора.
        :type archiver: str
        :param encryptor: Имя шифровальщика.
        :type encryptor: str
        :param exclude: Список исключений.
        :type exclude: [str]
        :param out: Поток вывода.
        :param err: Поток вывода сообщений об ошибках.
        """
        self.encoding = sys.getdefaultencoding()
        # Config
        if hasattr(config, 'config_file_path'):
            self.config_file_dir = os.path.dirname(
                getattr(config, 'config_file_path'))
        else:
            self.config_file_dir = None
        self.stream_out = sys.stdout if out is None else out
        self.stream_err = sys.stderr if err is None else err
        # Encryptor
        if encryptor is not None:
            encryptor_name = encryptor
        else:
            encryptor_name = config.get(
                self.SECTION, 'ENCRYPTOR', fallback=None)
        if encryptor_name is not None:
            self.encryptor = encrypt.make_encryptor(encryptor_name, config)
        else:
            self.encryptor = None
        # Archiver
        if archiver is not None:
            archiver_name = archiver
        else:
            archiver_name = config.get(
                self.SECTION,
                'ARCHIVER',
                fallback='tar',
            )
        self.archiver = archive.make_archiver(
            name=archiver_name,
            config=config,
            encryptor=self.encryptor,
        )
        # EXCLUDE parameter.
        exclude = kwargs.get('exclude', [])
        exclude_conf = config.get(self.SECTION, 'EXCLUDE', fallback=None)
        if exclude_conf is not None:
            exclude.extend(utils.dequote(exclude_conf).split(','))
        self.exclude = exclude if len(exclude) > 0 else None
        # EXCLUDE_FROM parameter.
        exclude_from = kwargs.get('exclude_from', [])
        exclude_from_conf = config.get(
            self.SECTION,
            'EXCLUDE_FROM',
            fallback=None,
        )
        if exclude_from_conf is not None:
            for exf in utils.dequote(exclude_from_conf).split(','):
                exf = utils.dequote(exf)
                if exf == '':
                    continue
                if not os.path.isabs(exf):
                    exf = os.path.abspath(
                        os.path.join(self.config_file_dir, exf))
                exclude_from.append(exf)
        self.exclude_from = exclude_from if len(exclude_from) > 0 else None
        # File methods.
        self.open = open
        self.compressor_cmd = None

    def _load_exclude_file(self, filepath):
        """Загрузка файла с шаблонами исключения из архива в список строк."""
        exclude_from = filepath
        if (not os.path.isabs(exclude_from)
                and self.config_file_dir is not None):
            exclude_from = os.path.join(
                self.config_file_dir,
                exclude_from,
            )
        exclude = []
        with open(exclude_from, 'r') as ex_file:
            for line in ex_file.readlines():
                exv = utils.dequote(line.strip())
                if exv != '':
                    exclude.append(exv)
        return exclude

    def _compress(self, in_stream, out_stream):
        """Сжатие потока in_stream в выходной поток out_stream."""
        compressor = subprocess.Popen(
            self.compressor_cmd,
            check=True,
            stdin=in_stream,
            stdout=out_stream,
            stderr=subprocess.PIPE,
        )
        in_stream.close()
        compressor.check_call()

    def outpath(self, archive_dir, name):
        """
        Generate archive file name.

        :param archive_dir: Path to archive directory.
        :type archive_dir: str
        :param name: Name of archive file without extensions.
        :type name: str
        :return: Full path to archive file.
        :rtype: str
        """
        fname = name + self.archiver.suffix
        return os.path.join(archive_dir, fname)

    @abc.abstractmethod
    def archive(self, source, output, base_dir=None):
        """
        Archive object.

        :param source: Source identifier.
        :type source: str
        :param output: Path to archive file.
        :type output: str
        :param base_dir: Path to base directory of source.
        :type base_dir: str
        :return: Exit code.
        :rtype: int
        """

    @abc.abstractmethod
    def backup(self, source, archive_dir, verbose=False):
        """
        Backup object.

        :param source: Source identifier.
        :type source: str
        :param archive_dir: Path to archive directory.
        :type archive_dir: str
        :param verbose: Print verbose messages.
        :type verbose: bool
        """

    def out(self, *args):
        """Output data to standard stream."""
        for data in args:
            if isinstance(data, bytes):
                data = data.decode(self.encoding)
            self.stream_out.write(data)
        else:
            self.stream_out.write('\n')

    def err(self, *args):
        """Output data to error stream."""
        for data in args:
            if isinstance(data, bytes):
                data = data.decode(self.encoding)
            self.stream_err.write(data)
        else:
            self.stream_err.write('\n')


class File(Base):
    """Архиватор файлов и папок."""

    SECTION = 'Backend-File'

    def archive(self, source, output, base_dir=None, exclude=None):
        """
        Архивировать один файл или папку.

        :param source: Путь к архивируемому файлу или папке.
        :type source: str
        :param output: Путь к файлу с архивом.
        :type output: str
        :param base_dir: Путь к базовой папке источников архивации.
        :type base_dir: str
        :param exclude: Дополнительный список исключений из архива.
        :type exclude: [str]
        """
        params = {
            'source': source,
            'output': output,
            'base_dir': base_dir,
        }
        ex = []
        if self.exclude is not None:
            ex.extend(self.exclude)
        if exclude is not None:
            ex.extend(exclude)
        if len(ex) != 0:
            params['exclude'] = ex
        if self.exclude_from is not None:
            params['exclude_from'] = self.exclude_from
        self.archiver.pack(**params)

    def backup(self, source, archive_dir, verbose=False):
        """
        Архивация файла или папки.

        :param source: Путь к архивируемому файлу или папке.
        :type source: str
        :param archive_dir: Путь к папке с архивами.
        :type archive_dir: str
        :param verbose: Выводить информационные сообщения.
        :type verbose: bool
        :return: Количество ошибок.
        :rtype: int
        """
        name = os.path.basename(source)
        if name == '':
            name = os.uname().nodename
        output = self.outpath(archive_dir, name=name)
        base_dir = None
        if os.path.isfile(source):
            stype = 'file'
            base_dir = os.path.dirname(source)
            source = os.path.basename(source)
        else:
            stype = 'directory'
        if verbose:
            self.out('Backup ', stype, ': ', source)
        try:
            self.archive(
                source=source,
                output=output,
                base_dir=base_dir,
                exclude=archive_dir,
            )
        except subprocess.CalledProcessError as ex:
            self.err(ex.stderr)
            return 1
        return 0


class Subversion(Base):
    """Архиватор репозиториев системы контроля версий Subversion."""

    SECTION = 'Backend-Subversion'

    def __init__(self, config, **kwargs):
        """Конструктор."""
        super().__init__(config, **kwargs)
        self.svnadmin_cmd = config.get(
            self.SECTION,
            'SVNADMIN_COMMAND',
            fallback='/usr/bin/svnadmin',
        )
        # compressor
        self.compressor_cmd = [config.get(
            self.SECTION,
            'COMPRESSOR_COMMAND',
            fallback='/bin/gzip',
        )]
        compressor_params = config.get(
            self.SECTION,
            'COMPRESSOR_PARAMS',
            fallback='-q9',
        ).split(' ')
        self.compressor_cmd.extend(compressor_params)
        self.compressor_suffix = config.get(
            self.SECTION,
            'COMPRESSOR_SUFFIX',
            fallback='.gz',
        )
        # exclude_from
        if self.exclude_from is not None:
            exclude = self.exclude if self.exclude is not None else []
            for exf in self.exclude_from:
                exclude.extend(self._load_exclude_file(exf))
            self.exclude = exclude if len(exclude) > 0 else None
            self.exclude_from = None

    def outpath(self, archive_dir, name):
        """
        Формирование имени файла архива.

        :param archive_dir: Путь к папке с архивами.
        :type archive_dir: str
        :param name: Имя архива без расширения.
        :type name: str
        :return: Полный путь к файлу архива.
        :rtype: str
        """
        fname = name + '.svn' + self.compressor_suffix
        return os.path.join(archive_dir, fname)

    def archive(self, source, output):
        """
        Архивация одного репозитория системы контроля версий Subversion.

        :param source: Путь к репозиторию.
        :type source: str
        :param output: Путь к файлу с архивом.
        :type output: str
        """
        name = os.path.basename(source)
        repo_copy_dir = tempfile.mkdtemp()
        repo_copy = os.path.join(repo_copy_dir, name)
        subprocess.run(
            [self.svnadmin_cmd, 'hotcopy', '--clean-logs', source,
                repo_copy],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=True,
        )
        tmp_path = output + '.tmp'
        p1 = subprocess.Popen(
            [self.svnadmin_cmd, 'dump', '--quiet', '--deltas', repo_copy],
            stdout=subprocess.PIPE,
        )
        try:
            with self.open(tmp_path, 'wb') as out:
                self._compress(in_stream=p1.stdout, out_stream=out)
        except subprocess.CalledProcessError:
            raise
        finally:
            shutil.rmtree(repo_copy_dir, ignore_errors=True)
        if self.encryptor is not None:
            output += self.encryptor.suffix
            try:
                self.encryptor.encrypt(tmp_path, output)
            except subprocess.CalledProcessError:
                raise
            finally:
                os.remove(tmp_path)
        else:
            shutil.move(tmp_path, output)
        os.chmod(output, self.archiver.ARCHIVE_PERMISSIONS)

    def backup(self, source, archive_dir, verbose=False):
        """
        Архивация всех репозиториев Subversion, находящихся в заданной папке.

        :param repos_dir: Путь к папке с репозиториями.
        :type repos_dir: str
        :param archive_dir: Путь к папке с архивами.
        :type archive_dir: str
        :param verbose: Выводить информационные сообщения.
        :type verbose: bool
        :return: Количество ошибок.
        :rtype: int
        """
        error_count = 0
        for repo in os.listdir(source):
            if (self.exclude is not None and repo in self.exclude):
                if verbose is True:
                    self.out('Exclude repo: ', repo)
                continue
            repo_path = os.path.join(source, repo)
            if not os.path.isdir(repo_path):
                continue
            svnfmt = os.path.join(repo_path, 'format')
            if not (os.path.exists(svnfmt) and os.path.isfile(svnfmt)):
                continue
            if verbose is True:
                self.out('Backup repo: ', repo)
            try:
                self.archive(repo_path, self.outpath(archive_dir, repo))
            except subprocess.CalledProcessError as ex:
                error_count += 1
                self.err(ex.stderr)
        return error_count


class Mercurial(Base):
    """Архиватор репозиториев системы контроля версий Mercurial."""

    SECTION = 'Backend-Mercurial'

    def __init__(self, config, **kwargs):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        """
        super().__init__(config, **kwargs)
        # exclude_from
        if self.exclude_from is not None:
            exclude = self.exclude if self.exclude is not None else []
            for exf in self.exclude_from:
                exclude.extend(self._load_exclude_file(exf))
            self.exclude = exclude if len(exclude) > 0 else None
            self.exclude_from = None

    def archive(self, source, output):
        """
        Архивация одного репозитория системы контроля версий Mercurial.

        :param source: Путь к репозиторию Mercurial.
        :type source: str
        :param output: Путь к файлу архива.
        :type output: str
        """
        name = os.path.basename(source)
        repo_bak_dir = tempfile.mkdtemp()
        repo_bak = os.path.join(repo_bak_dir, name)
        subprocess.run(
            ['/usr/bin/hg', 'clone', '--noupdate', '--quiet',
             source, repo_bak],
            stdout=self.stream_out,
            stderr=self.stream_err,
            check=True,
        )
        try:
            self.archiver.pack(name, output, repo_bak_dir)
        except subprocess.CalledProcessError:
            raise
        finally:
            shutil.rmtree(repo_bak_dir, ignore_errors=True)

    def backup(self, source, archive_dir, verbose=False):
        """
        Архивация всех репозиториев Mercurial в заданной папке.

        :param repos_dir: Путь к папке с репозиториями.
        :type repos_dir: str
        :param archive_dir: Путь к папке с архивами.
        :type archive_dir: str
        :param verbose: Выодить информационные сообщения.
        :type verbose: bool
        :return: Количество ошибок.
        :rtype: int
        """
        error_count = 0
        for repo in os.listdir(source):
            if self.exclude is not None and repo in self.exclude:
                if verbose:
                    self.out('Exclude repo: ', repo)
                continue
            repo_path = os.path.join(source, repo)
            if not os.path.isdir(repo_path):
                continue
            hgdir = os.path.join(repo_path, '.hg')
            if not (os.path.exists(hgdir) and os.path.isdir(hgdir)):
                continue
            if verbose:
                self.out('Backup repo: ', repo)
            try:
                self.archive(
                    source=repo_path,
                    output=self.outpath(
                        archive_dir,
                        os.path.basename(repo_path),
                    ),
                )
            except subprocess.CalledProcessError as ex:
                error_count += 1
                self.err(ex.stderr)
        return error_count


class PostgreSQL(Base):
    """Архиватор баз данных PostgreSQL."""

    SECTION = 'Backend-PostgreSQL'

    FORMAT_NONE = 0  # Формат архива не задан.
    FORMAT_PLAIN = 1  # Полный архив БД в текстовом формате.
    FORMAT_CUSTOM = 2  # Полный архив БД в сжатом формате.

    FORMAT_MAP = {
        'plain': FORMAT_PLAIN,
        'custom': FORMAT_CUSTOM,
        'default': FORMAT_NONE,
    }

    MODE_NONE = 0  # Запрет архивирования БД.
    MODE_SCHEMA = 1  # Архивировать только схему БД.
    MODE_FULL = 2  # Полный архив БД.

    def __init__(self, config, **kwargs):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param out: Поток вывода информационных сообщений.
        :param err: Поток вывода сообщений об ошибках.
        :param encryptor: Имя шифровальщика.
        :type encryptor: str
        """
        super().__init__(config, **kwargs)
        # hostname
        self.hostname = config.get(
            self.SECTION,
            'HOSTNAME',
            fallback=None,
        )
        # port
        self.port = config.get(
            self.SECTION,
            'PORT',
            fallback=None,
        )
        # username
        self.username = config.get(
            self.SECTION,
            'USERNAME',
            fallback=None,
        )
        # format
        format_name = config.get(
            self.SECTION,
            'BACKUP_FORMAT',
            fallback='plain',
        )
        if format_name in self.FORMAT_MAP:
            self.format = self.FORMAT_MAP[format_name]
        else:
            raise Exception('Invalid backup format name: {}'
                            .format(format_name))
        # schema_only_list
        self.schema_only_list = []
        lst = utils.dequote(config.get(
            self.SECTION,
            'SCHEMA_ONLY_LIST',
            fallback=utils.EmptyListString(),
        ))
        self.schema_only_list.extend(lst.split(' '))
        # psql_cmd
        self.psql_cmd = config.get(
            self.SECTION,
            'PSQL_COMMAND',
            fallback='/usr/bin/psql',
        )
        # pgdump_cmd
        self.pgdump_cmd = config.get(
            self.SECTION,
            'PGDUMP_COMMAND',
            fallback='/usr/bin/pg_dump',
        )
        # compressor
        self.compressor_cmd = [config.get(
            self.SECTION,
            'COMPRESSOR_COMMAND',
            fallback='/bin/gzip',
        )]
        compressor_params = config.get(
            self.SECTION,
            'COMPRESSOR_PARAMS',
            fallback='-q9',
        ).split(' ')
        self.compressor_cmd.extend(compressor_params)
        self.compressor_suffix = config.get(
            self.SECTION,
            'COMPRESSOR_SUFFIX',
            fallback='.gz',
        )
        # exclude_from
        if self.exclude_from is not None:
            exclude = self.exclude if self.exclude is not None else []
            for exf in self.exclude_from:
                exclude.extend(self._load_exclude_file(exf))
            self.exclude = exclude if len(exclude) > 0 else None
            self.exclude_from = None

    def outpath(self, archive_dir, name, mode=MODE_NONE):
        """
        Формирование имени файла с архивом.

        :param archive_dir: Путь к папке с архивами.
        :type archive_dir: str
        :param name: Имя файла архива без расширения.
        :type name: str
        :return: Полный путь к файлу с архивом.
        :rtype: str
        """
        fname = name
        if mode == self.MODE_SCHEMA:
            fname += '_SCHEMA.sql'
            fname += self.compressor_suffix
        elif self.format == self.FORMAT_PLAIN:
            fname += '.sql'
            fname += self.compressor_suffix
        elif self.format == self.FORMAT_CUSTOM:
            fname += '.custom'
        else:
            fname += self.compressor_suffix
        return os.path.join(archive_dir, fname)

    def archive(self, source, output, mode=MODE_NONE):
        """
        Архивация одной базы данных PostgreSQL.

        :param source: Имя базы данных.
        :type source: str
        :param output: Путь к файлу с архивом.
        :type output: str
        :param mode: Режим архивации.
        :type mode: int
        """
        tmp_path = output + self.archiver.progress_suffix
        if self.format == self.FORMAT_CUSTOM:
            self.dump_proc(
                database=source,
                output=tmp_path,
                mode=mode,
            ).check_call()
        else:
            p1 = self.dump_proc(
                database=source,
                output=tmp_path,
                mode=mode,
                stdout=subprocess.PIPE,
            )
            with self.open(tmp_path, 'wb') as out:
                self._compress(in_stream=p1.stdout, out_stream=out)
        if self.encryptor is not None:
            try:
                self.encryptor.encrypt(
                    source=tmp_path,
                    output=output + self.encryptor.suffix,
                )
            except subprocess.CalledProcessError:
                raise
            finally:
                os.remove(tmp_path)
        else:
            shutil.move(tmp_path, output)

    def backup(self, source, archive_dir, verbose=False):
        """
        Архивация всех баз данных PostgreSQL на заданном узле.

        :param source: Узел сервера PostgreSQL или путь к сокету.
        :type source: str
        :param archive_dir: Путь к папке с архивами.
        :type archive_dir: str
        :param base_dir: Путь к папке с источниками (игнорируется).
        :type base_dir: str
        :param verbose: Выводить информационные сообщения.
        :type verbose: bool
        :return: Количество ошибок.
        :rtype: int
        """
        dblist = [source] if source is not None else self.dblist()
        error_count = 0
        for database in dblist:
            if self.exclude is not None and database in self.exclude:
                if verbose is True:
                    self.out('Exclude database: ', database)
                continue
            mode = (self.MODE_SCHEMA if database in self.schema_only_list
                    else self.MODE_FULL)
            if verbose is True:
                info = ''
                if mode == self.MODE_SCHEMA:
                    info = 'Schema-only'
                elif self.format == self.FORMAT_PLAIN:
                    info = 'Plain'
                elif self.format == self.FORMAT_CUSTOM:
                    info = 'Custom'
                else:
                    info = 'Default'
                self.out(info, ' backup database: ', database)
            try:
                self.archive(
                    source=database,
                    output=self.outpath(archive_dir, database, mode),
                    mode=mode,
                )
            except subprocess.CalledProcessError as ex:
                error_count += 1
                self.err(ex.stderr)
        return error_count

    def dblist(self):
        """
        Database list on the target host.

        :return: List of all databases.
        :rtype: list
        """
        params = [self.psql_cmd]
        if self.hostname:
            params.append('--host={}'.format(self.hostname))
        if self.port:
            params.append('--port={}'.format(self.port))
        if self.username:
            params.append('--username={}'.format(self.username))
        params.append('--no-password')
        params.append('--no-align')
        params.append('--tuples-only')
        params.append('-c')
        params.append('SELECT datname '
                      'FROM pg_database '
                      'WHERE NOT datistemplate '
                      'ORDER BY datname;')
        params.append('postgres')
        out = subprocess.check_output(params)
        return out.decode(sys.getdefaultencoding()).splitlines()

    def dump_proc(self, database, output, mode, **kwargs):
        """
        Create process of dump PostgreSQL database.

        :param database: Database name.
        :type database: str
        :param output: Path to archive file.
        :type output: str
        :param mode: Database backup mode.
        :type mode: int
        :param **kwargs: Arguments of `subprocess.Popen()` constructor.
        :type **kwargs: dict
        """
        params = [self.pgdump_cmd]
        if mode == self.MODE_SCHEMA or self.format == self.FORMAT_PLAIN:
            params.append('--format=p')
        elif self.format == self.FORMAT_CUSTOM:
            params.append('--format=c')
        if mode == self.MODE_SCHEMA:
            params.append('--schema-only')
        if self.hostname:
            params.append('--host={}'.format(self.hostname))
        if self.port:
            params.append('--port={}'.format(self.port))
        if self.username:
            params.append('--username={}'.format(self.username))
        params.append('--no-password')
        params.append('--oids')
        if self.format == self.FORMAT_CUSTOM:
            params.append('--file={}'.format(output))
        params.append(database)
        return subprocess.Popen(params, **kwargs)


BACKENDS = {
    'file': File,
    'subversion': Subversion,
    'mercurial': Mercurial,
    'postgresql': PostgreSQL,
}


def make_backend(name, config, **kwargs):
    """
    Create back-end object.

    :param name: Name of back-end to create.
    :type name: str
    :param config: Config object.
    :type config: :class:`ConfigParser.RawConfigParser`
    """
    if name not in BACKENDS:
        raise Exception('Unknown back-end: {}'.format(name))
    return BACKENDS[name](config=config, **kwargs)
