# coding: utf-8
from django.core.management import BaseCommand
from subprocess import check_call, check_output
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            # Generate django translations
            check_call("python manage.py makemessages -l en -i '**/node_modules' -i 'node_modules' -i 'env'",
                       shell=True)

            # Generate template's metadata translation strings
            check_call("python manage.py makethememessages -o themes.po", shell=True)

            # Download existing strings
            check_call("crowdin-cli-py download -l en", shell=True)

            # Merge all message files into a single one containing all translation strings
            check_call(
                "python manage.py mergemessages -o {out} locale/en/LC_MESSAGES/{out} locale/en/LC_MESSAGES/django.po themes.po po/additional.po".format(
                    out=settings.CROWDIN_CONSOLIDATED_FILE), shell=True)

            # Upload sources for translations to crowdin
            check_call("crowdin-cli-py upload sources", shell=True)

            # Remove all local po files
            check_call("find locale -type f -iname '*.po' |xargs -n1 rm", shell=True)

        finally:
            # Cleanup temp files
            check_call("rm -f themes.po {out}".format(out=settings.CROWDIN_CONSOLIDATED_FILE), shell=True)

