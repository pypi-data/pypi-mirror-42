# coding=utf-8
from django.core.management import BaseCommand
from subprocess import check_call


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Download existing translations from crowdin
        check_call("crowdin-cli-py download", shell=True)

        # Remove locales we don't need (and cause compilemessages to crash)
        check_call("find locale/de -type f -iname '*.po'|xargs -n1 rm", shell=True)

        # Rename files so that django con find them
        check_call("find locale/ -name '*.po' -execdir mv -f {} django.po \;", shell=True)

        # Compile messages
        check_call("python manage.py compilemessages", shell=True)

        # Remove all po files (which can be generated with makemessages)
        check_call("find locale/ -type f -iname '*.po'|xargs -n1 rm", shell=True)

