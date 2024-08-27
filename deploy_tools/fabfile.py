import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/vitormsantana/python-tdd-book.git'
env.key_filename = 'C:/Users/vitor/OneDrive/Documentos/python/oreilly/tdd-key.pem'

def deploy():
    #site_folder = f'/home/{env.user}/sites/{env.host}'
    #site_folder = f'/home/sites/{env.host}'
    #site_folder = f'/home/sites/python-tdd-book'
    site_folder = f'/home/sites/vifevi-tdd.online'
    if not exists(site_folder):
        run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        print(f'now, run {_get_latest_source} \n----------\n')
        _get_latest_source()
        print(f'now, run {_update_virtualenv} \n----------\n')
        _update_virtualenv()
        print(f'now, run {_create_or_update_dotenv} \n----------\n')
        _create_or_update_dotenv()
        print(f'now, run {_update_static_files} \n----------\n')
        _update_static_files()
        print(f'now, run {_update_database} \n----------\n')
        _update_database()

def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')

def _update_virtualenv():
    if not exists('.venv_linux2/bin/pip'):
        run(f'python3.6 -m venv venv_linux2')
    run('./.venv_linux2/bin/pip install -r requirements-dev.txt')

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
    run('./.venv_linux2/bin/python manage.py collectstatic --noinput')

def _update_database():
    run('./.venv_linux2/bin/python manage.py migrate --noinput')
