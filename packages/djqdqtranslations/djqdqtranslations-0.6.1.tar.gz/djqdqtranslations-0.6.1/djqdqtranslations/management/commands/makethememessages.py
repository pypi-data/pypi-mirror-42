import optparse
import unipath
import json
from django.conf import settings
from django.core.management import BaseCommand
from django.core.exceptions import ImproperlyConfigured
from polib import POEntry, POFile


class ThemeTranslationsException(Exception):
    pass


class Command(BaseCommand):

    try:
        default_repo = settings.THEMES_REPOS
    except ImproperlyConfigured:
        default_repo = None

    option_list = BaseCommand.option_list + (
        optparse.make_option('-r', '--repo',
                             help='Path to repository containing themes', default=default_repo),
        optparse.make_option('-o', '--output', help='Output file', default='themes.po')
    )

    def handle(self, *args, **options):
        po_file = POFile(check_for_duplicates=True)
        po_file.metadata = {
            'Project-Id-Version': '1.0',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }
        for repo_path in options.get('repo', []):
            entries = _get_package_entries(repo_path)
            for entry in entries:
                if not entry in po_file:
                    po_file.append(entry)
        po_file.save(fpath=options.get('output'))


def _iter_package_files(repo):
    possible_locations = (('build', 'package.json'), ('package.json',))
    for package_dir in unipath.Path(repo).listdir(filter=unipath.DIRS):
        found = False
        for location in possible_locations:
            package_json = package_dir.child(*location)
            if package_json.exists():
                found = True
                yield package_json
                continue
        if not found:
            raise ThemeTranslationsException(
                    "Can't find theme configuration file in {}".format(package_dir))


def _get_package_entries(repo):
    entries = []
    for package_json in _iter_package_files(repo):
        try:
            with open(package_json) as data:
                metadata = json.loads(data.read())
        except ValueError as e:
            raise ThemeTranslationsException(
                "Can't read theme configuraton file {} : {}".format(package_json, e.message))
        if 'data' not in metadata or not type(metadata['data']) == dict:
            continue
        data = metadata.get('data', {})
        if 'translate' not in data:
            continue
        translate = data.get('translate')
        path = u"package_json/{author}/{name}/{version}".format(
            author=metadata.get('author'),
            name=metadata.get('name'),
            version=metadata.get('version')
        )
        occurrence = (path, u'1')
        if type(translate) != list:
            raise ThemeTranslationsException("'translate' section must be a list of strings or objects")
        for field in translate:
            for string in _get_strings(field, data):
                if string:
                    entries.append(POEntry(msgid=string, msgstr=string, occurrences=[occurrence]))
    return entries


def _get_strings(field, data):
    strings = []
    if isinstance(field, basestring):
        strings.append(data.get(field, None))
    elif type(field) == int:
        try:
            strings.append(data[field])
        except KeyError:
            raise ThemeTranslationsException("Can't access field {} of {}".format(field, data))
    elif type(field) == dict:
        for k, v in field.items():
            if k == '*':
                if type(data) == list:
                    for element in data:
                        strings.extend(_get_strings(v, element))
                elif type(data) == dict:
                    for element in data.keys():
                        strings.extend(_get_strings(v, data[element]))
                else:
                    raise ThemeTranslationsException("List expected but got {} instead".format(data))
            elif k in data:
                strings.extend(_get_strings(v, data[k]))
    return strings
