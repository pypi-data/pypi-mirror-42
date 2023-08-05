
from .utils import get_source_revision


REVISION = get_source_revision()


def static_revision(request):
    return {'REVISION': REVISION}
