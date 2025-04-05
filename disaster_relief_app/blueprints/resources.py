from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Resource, AuditLog

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/resources', methods=['GET', 'POST'])
@login_required
def manage_resources():
    if request.method == 'POST':
        resource_type = request.form.get('resource_type')
        quantity = int(request.form.get('quantity'))
        location = request.form.get('location')
        resource = Resource(resource_type=resource_type, quantity=quantity, location=location)
        db.session.add(resource)
        db.session.commit()
        log = AuditLog(user_id=current_user.id, action="Added Resource", details=f"{resource_type} x {quantity}")
        db.session.add(log)
        db.session.commit()
        flash("Resource added", "success")
        return redirect(url_for('resources.manage_resources'))
    resources = Resource.query.all()
    return render_template('resources.html', resources=resources)
