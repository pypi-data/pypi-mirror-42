import optparse
from unipath import Path
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from polib import POFile, pofile, POEntry


class ThemeTranslationsException(Exception):
    pass


class ConservativePOFile(POFile):
    """
    Subclass of POFile which doesn't mark entries as obsolete after a merge
    """

    def merge(self, refpot):
        # Merge entries that are in the refpot
        for entry in refpot:
            if entry not in self:
                self.append(entry)
            else:
                e = self.find(entry.msgid, msgctxt=entry.msgctxt)
                e.merge(entry)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        optparse.make_option('-o', '--output',
                             help='Output file', default=settings.CROWDIN_CONSOLIDATED_FILE),
    )

    def handle(self, *args, **options):

        if not args:
            raise CommandError('Please, provide a list of po files to merge')
        out_path = Path(options.get('output', 'out.po'))
        out_po = ConservativePOFile()
        out_po.metadata = {
            'Project-Id-Version': '1.0',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }

        for po_path in args:
            path = Path(po_path)
            if not path.exists():
                raise CommandError('File not found: {}'.format(path))
            po_file = pofile(po_path)
            out_po.merge(po_file)
        out_po.save(out_path)

