from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, VolunteerTask, AuditLog

volunteer_bp = Blueprint('volunteer', __name__)

@volunteer_bp.route('/dashboard')
@login_required
def dashboard():
    tasks = VolunteerTask.query.filter_by(assigned_to=current_user.id).all()
    return render_template('volunteer_dashboard.html', tasks=tasks)

@volunteer_bp.route('/accept_task/<int:task_id>', methods=['POST'])
@login_required
def accept_task(task_id):
    task = VolunteerTask.query.get_or_404(task_id)
    task.assigned_to = current_user.id
    db.session.commit()
    log = AuditLog(user_id=current_user.id, action="Accepted Task", details=f"Task ID {task_id}")
    db.session.add(log)
    db.session.commit()
    flash("Task accepted", "success")
    return redirect(url_for('volunteer.dashboard'))

@volunteer_bp.route('/update_task_status/<int:task_id>', methods=['POST'])
@login_required
def update_task_status(task_id):
    new_status = request.form.get('status')
    task = VolunteerTask.query.get_or_404(task_id)
    task.status = new_status
    db.session.commit()
    log = AuditLog(user_id=current_user.id, action="Updated Task", details=f"Task ID {task_id} updated to {new_status}")
    db.session.add(log)
    db.session.commit()
    flash("Task status updated", "success")
    return redirect(url_for('volunteer.dashboard'))
