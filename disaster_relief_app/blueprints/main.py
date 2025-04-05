from flask import Blueprint, render_template, redirect, url_for, flash, request
from disaster_relief_app.models import db, HelpRequest, AuditLog


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    requests = HelpRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', requests=requests)

@main_bp.route('/request', methods=['GET', 'POST'])
@login_required
def create_request():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_req = HelpRequest(title=title, description=description, user_id=current_user.id)
        db.session.add(new_req)
        db.session.commit()
        log = AuditLog(user_id=current_user.id, action="Created Request", details=title)
        db.session.add(log)
        db.session.commit()
        flash("Help request submitted", "success")
        return redirect(url_for('main.dashboard'))
    return render_template('create_request.html')

@main_bp.route('/update_progress/<int:request_id>', methods=['POST'])
@login_required
def update_progress(request_id):
    req = HelpRequest.query.get_or_404(request_id)
    if req.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('main.dashboard'))
    try:
        progress = int(request.form.get('progress'))
        if 0 <= progress <= 100:
            req.progress = progress
            req.status = 'Resolved' if progress == 100 else ('In Progress' if progress > 0 else 'Pending')
            db.session.commit()
            flash("Progress updated", "success")
        else:
            flash("Invalid progress value", "danger")
    except (ValueError, TypeError):
        flash("Invalid input", "danger")
    return redirect(url_for('main.dashboard'))
