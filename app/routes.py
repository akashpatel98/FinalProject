from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import current_user, logout_user
from flask import current_app as app
from .assets import compile_auth_assets
from flask_login import login_required


main_bp = Blueprint(
    'main_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)
compile_auth_assets(app)


@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Logged in Dashboard screen."""
    session['redis_test'] = 'This is a session variable.'
    return render_template(
        'dashboard.jinja2',
        title='Flask-Session Tutorial.',
        template='dashboard-template',
        current_user=current_user,
        body="You are now logged in!"
    )


@main_bp.route('/session', methods=['GET'])
@login_required
def session_view():
    """Display session variable value."""
    return render_template(
        'session.jinja2',
        title='Flask-Session Tutorial.',
        template='dashboard-template',
        session_variable=str(session['redis_test'])
    )

@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))


@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard.jinja2',
        title='Flask-Login Tutorial.',
        template='dashboard-template',
        current_user=current_user,
        body="You are now logged in!"
    )
routes.py


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))


@app.route('/', methods=['GET'])
def user_records():
    """Create a user via query string parameters."""
    username = request.args.get('user')
    email = request.args.get('email')
    if username and email:
        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            bio="In West Philadelphia born and raised, \
            on the playground is where I spent most of my days",
            admin=False
        )
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
    return make_response(f"{new_user} successfully created!")


@app.route('/', methods=['GET'])
def user_records():
    """Create a user via query string parameters."""
    username = request.args.get('user')
    email = request.args.get('email')
    if username and email:
        existing_user = User.query.filter(
            User.username == username or User.email == email
        ).first()
        if existing_user:
            return make_response(
                f'{username} ({email}) already created!'
            )
        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            bio="In West Philadelphia born and raised, \
            on the playground is where I spent most of my days",
            admin=False
        )  # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for('user_records'))
    return render_template(
        'users.jinja2',
        users=User.query.all(),
        title="Show Users"
    )


@app.route('/')
def home():
    """Landing page."""
    nav = [
        {'name': 'Home', 'url': 'https://example.com/1'},
        {'name': 'About', 'url': 'https://example.com/2'},
        {'name': 'Pics', 'url': 'https://example.com/3'}
    ]
    return render_template(
        'home.html',
        nav=nav,
        title="Jinja Demo Site",
        description="Smarter page templates with Flask & Jinja."
    )