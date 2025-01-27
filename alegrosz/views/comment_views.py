from flask import Blueprint, url_for
from werkzeug.utils import escape, redirect

from ..dbs.dbs import get_db
from ..forms.comment_forms import CommentForm

bp_comment = Blueprint("comment", __name__, url_prefix='/comments')


@bp_comment.route('/', methods=['POST'])
def comment():
    conn = get_db()
    c = conn.cursor()

    form = CommentForm()

    if form.validate_on_submit():
        c.execute('''INSERT INTO comment (content, item_id)
         VALUES (?,?)
        ''', (
            escape(form.content.data),
            form.item_id.data
        ))

        conn.commit()
    return redirect(url_for('item.item', item_id=form.item_id.data))
