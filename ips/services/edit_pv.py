import io
import os
import zipfile

from flask import request, render_template, Blueprint, session, redirect, send_file, abort, Response
from flask_login import login_required

from ips.util.ui_logging import log

bp = Blueprint('edit pv', __name__, url_prefix='', static_folder='static')


@bp.route('/edit_pv', methods=['GET', 'POST'])
@bp.route('/edit_pv/<run_id>', methods=['GET', 'POST'])
@bp.route('/edit_pv/<run_id>/<template_id>', methods=['GET', 'POST'])
@login_required
def edit_pv(run_id, template_id=None):
    log.debug(f"edit_pv called - run_id: {run_id}")
    print("rennnnderrrr edit_pv")
    return render_template('edit_pv.html', run_id=run_id)
