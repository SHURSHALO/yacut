from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.form import UrlForm
from yacut.models import URLMap
from yacut.utilis import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        short_id = get_unique_short_id(form.custom_id.data)

        if URLMap.is_short_url_exists(short_id):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)

        url = URLMap(
            original=form.original_link.data,
            short=short_id,
        )

        db.session.add(url)

        db.session.commit()

        return render_template('yacut.html', form=form, url=url)
    return render_template('yacut.html', form=form)


@app.route('/<short_id>')
def redirect_to_original(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map:
        return redirect(url_map.original)
    abort(404)
