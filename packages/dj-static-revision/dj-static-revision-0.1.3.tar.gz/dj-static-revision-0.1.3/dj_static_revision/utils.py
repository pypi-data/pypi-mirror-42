import logging
from pathlib import Path

from dulwich.repo import Repo


FILE_NAME_REVISION = '.version'
REVISION_LENGTH = 7
logger = logging.getLogger(__name__)


def locate_django_manage():
    '''
    Locate project's manage.py file
    '''
    folder = Path.cwd()
    # Look for manage.py in current folder or up
    for i in range(5):
        p = folder / 'manage.py'
        if p.exists():
            return folder
        folder = folder.parent
    raise FileNotFoundError('Django manage.py file not found')


def get_source_revision_from_git(folder):
    dot_git = folder / '.git'
    if not dot_git.is_dir():
        raise OSError('Not a Git working copy')
    repo = Repo(folder)
    # We truncate the hash string to 7 characters,
    # that is also the way Git represents in short form.
    return repo.head()[:REVISION_LENGTH].decode()


def get_source_revision_from_text_file(folder):
    path = folder / FILE_NAME_REVISION
    try:
        content = path.read_text().strip()
    except IOError:
        logger.error('Failed to read {}'.format(path))
        return 'version-file-missing'
    return content[:REVISION_LENGTH]


def get_source_revision():
    folder = locate_django_manage()
    if (folder / FILE_NAME_REVISION).exists():
        return get_source_revision_from_text_file(folder)
    return get_source_revision_from_git(folder)
