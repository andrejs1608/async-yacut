from flask import flash, redirect, render_template, url_for

from . import app, db
from .constants import UPLOAD_ERROR
from .forms import UploadFilesForm, URLMapForm
from .models import URLMap
from .yadisk import upload_files_to_yadisk


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    custom_id = form.custom_id.data

    if custom_id:
        if (
            URLMap.query.filter_by(short=custom_id).first()
            or custom_id == 'files'
        ):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
    else:
        custom_id = URLMap.get_unique_short_id()

    url_map = URLMap(original=form.original_link.data, short=custom_id)
    db.session.add(url_map)
    db.session.commit()

    short_url = url_for(
        'redirect_short', short_id=url_map.short, _external=True
    )

    return render_template(
        'index.html',
        form=form,
        short_url=short_url
    )


@app.route('/files', methods=['GET', 'POST'])
async def file_upload_view():
    form = UploadFilesForm()

    if not form.validate_on_submit():
        return render_template('upload_files.html', form=form)

    try:
        yadisk_results = await upload_files_to_yadisk(form.files.data)

        file_links = []
        for file_info in yadisk_results:
            new_map = URLMap.create(file_info['url'])

            file_links.append((
                file_info['filename'],
                url_for(
                    'redirect_short', short_id=new_map.short, _external=True
                )
            ))

        return render_template(
            'upload_files.html',
            form=form,
            file_links=file_links
        )

    except Exception as exc:
        flash(UPLOAD_ERROR.format(str(exc)))
        return render_template('upload_files.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_short(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
