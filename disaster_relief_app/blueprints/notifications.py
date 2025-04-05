from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, AuditLog

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/send_notification', methods=['POST'])
@login_required
def send_notification():
    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('main.dashboard'))
    message = request.form.get('message')
    # Import socketio from the main app (ensure circular import is resolved)
    from app import socketio
    socketio.emit('notification', {'msg': message}, broadcast=True)
    log = AuditLog(user_id=current_user.id, action="Sent Notification", details=message)
    db.session.add(log)
    db.session.commit()
    flash("Notification sent", "success")
    return redirect(url_for('admin.admin_dashboard'))
