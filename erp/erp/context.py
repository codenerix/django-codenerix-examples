from django.conf import settings

from erp.common.helpers import get_POS


def project_context(request):
    info = get_POS(request)
    pos = info['POS']
    commit = info['commit']
    user = request.user

    if user.is_anonymous or user.username not in settings.INFO_PROJECT:
        info_project = settings.INFO_PROJECT_DEFAULT
    else:
        info_project = settings.INFO_PROJECT[user.username]

    return {
        'WEBSOCKET_URL': "{}:{}".format(request.META.get("HTTP_HOST").split(":")[0], settings.WEBSOCKET_PORT),
        'posname': getattr(pos, 'name', None),
        'commit': commit,
        'name_project': info_project['name_project'],
        'info_project': info_project
    }
