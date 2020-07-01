from flask import Blueprint, render_template
from flask_login import login_required

from ips.util.ui_logging import log
from ips.services.app_methods import get_run
from ips.services import app_methods, API_TARGET


bp = Blueprint('view_step_report', __name__, url_prefix='', static_folder='static')


@bp.route('/view_step_report/<run_id>/<step>', methods=['GET', 'POST'])
@login_required
def view_step_report(run_id=None, step=None):
    log.debug(f"view_step_report called - run_id: {run_id}")

    run = get_run(run_id)

    current_run = run
    step_status = app_methods.get_run_steps(run_id)[int(step) - 1]
    step_name = options[int(step)]

    return render_template('view_step_report.html', current_run=current_run, step_status=step_status, step_name=step_name)


options = {1: "Calculate Shift Weight",
           2: "Calculate Non-Response Weight",
           3: "Calculate Minimums Weight",
           4: "Calculate Traffic Weight",
           5: "Calculate Unsampled Weight",
           6: "Calculate Imbalance Weight",
           7: "Calculate Final Weight",
           8: "Stay Imputation",
           9: "Fares Imputation",
           10: "Spend Imputation",
           11: "Rail Imputation",
           12: "Regional Weight",
           13: "Town Stay and Expenditure Imputation",
           14: "Air Miles",
           }
