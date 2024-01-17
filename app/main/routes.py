from flask import render_template
from flask_login import login_required
from app.main import bp
from app.main.utils import (
    get_python_version,
    list_installed_packages,
    get_os_and_version,
    get_sqlite_version,
    get_cpu_info,
    get_ram_usage,
    get_cpu_usage,
    bytes_to_human_readable
)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.jinja2')


@bp.route('/administration')
@login_required
def administration():
    return render_template('administration/index.jinja2')


@bp.route('/administration/system')
@login_required
def system():
    return render_template('administration/system.jinja2',
                           python_version = get_python_version(),
                           python_packages=list_installed_packages(),
                           os_version =get_os_and_version(),
                           sqlite_info=get_sqlite_version(),
                           cpu_info=get_cpu_info(),
                           ram_total=bytes_to_human_readable(get_ram_usage()['total']))

@bp.route('/administration/system/poll-usage')
@login_required
def poll_usage():
    ram_info = get_ram_usage()
    total_ram = ram_info['total']  # Total RAM in bytes
    used_ram = ram_info['used']  # Used RAM in bytes
    ram_percentage = round((used_ram / total_ram) * 100)
    cpu = get_cpu_usage()
    return render_template('administration/system/_pollusage.jinja2', ram=ram_percentage, cpu=cpu)


