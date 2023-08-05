from .. import main


@main.group()
def admin():
    '''
    Provides the admin API access.
    '''


def _attach_command():
    from . import agents, images, keypairs, sessions, vfolders  # noqa


_attach_command()
