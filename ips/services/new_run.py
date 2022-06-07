from flask import Blueprint
from flask_login import login_required

from ips.services.new_run_steps.step_1 import run_step_1
from ips.services.new_run_steps.step_2 import run_step_2_m, run_step_2_q
from ips.services.new_run_steps.step_3 import run_step_3
from ips.services.new_run_steps.step_4 import run_step_4
from ips.services.new_run_steps.step_5 import run_step_5
from ips.util.ui_logging import log

bp = Blueprint('new_run_steps', __name__, url_prefix='/new_run_steps', static_folder='static')


@bp.route('/new_run_1', methods=['GET', 'POST'])
@bp.route('/new_run_1/<run_id>', methods=['GET', 'POST'])
@login_required
def new_run_1(run_id=None):
    log.debug(f"new_run_1 called - run_id: {run_id}")
    return run_step_1(run_id)


@bp.route('/new_run_2_m', methods=['GET', 'POST'])
@bp.route('/new_run_2_m/<run_id>', methods=['GET', 'POST'])
@login_required
def new_run_2_m(run_id=None):
    log.debug(f"new_run_2 called - run_id: {run_id}")
    return run_step_2_m(run_id)


@bp.route('/new_run_2_q', methods=['GET', 'POST'])
@bp.route('/new_run_2_q/<run_id>', methods=['GET', 'POST'])
@login_required
def new_run_2_q(run_id=None):
    log.debug(f"new_run_2 called - run_id: {run_id}")
    return run_step_2_q(run_id)


@bp.route('/new_run_3', methods=['GET', 'POST'])
@bp.route('/new_run_3/<run_id>', methods=['GET', 'POST'])
@login_required
def new_run_3(run_id=None):
    log.debug(f"new_run_3 called - run_id: {run_id}")
    return run_step_3(run_id)


@bp.route('/new_run_4', methods=['GET', 'POST'])
@bp.route('/new_run_4/<run_id>', methods=['GET', 'POST'])
@bp.route('/new_run_4/<run_id>/<template_id>', methods=['GET', 'POST'])
@login_required
def new_run_4(run_id=None, template_id=None):
    log.debug(f"new_run_4 called - run_id: {run_id}")
    return run_step_4(run_id, template_id)


@bp.route('/new_run_5', methods=['GET', 'POST'])
@bp.route('/new_run_5/<run_id>', methods=['GET', 'POST'])
@login_required
def new_run_5(run_id=None):
    log.debug(f"new_run_5 called - run_id: {run_id}")
    return run_step_5(run_id)

