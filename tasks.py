import nltk
from invoke import run, task


@task
def nltk_deps(context):
    nltk.download("punkt")


@task(pre=(nltk_deps,))
def build(context, folder_mode=False):
    run(
        f'pyinstaller \
--name=polysem_tyoplyi \
--noconfirm {"--onefile" if not folder_mode else ""} \
--icon "./ui/icons/favicon.ico" \
--add-data "./data;./data/" \
--add-data "./mystem.exe;." \
"./polysem.py"'
    )
