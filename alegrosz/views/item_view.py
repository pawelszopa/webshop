from flask import Blueprint, flash, url_for, render_template
from flask_wtf.file import FileRequired
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from ..forms.comment_forms import CommentForm
from ..helpers import save_image_upload
from ..dbs.dbs import get_db
from ..forms.item_forms import NewItemForm, EditItem, DeleteItem

bp_item = Blueprint("item", __name__, url_prefix='/items')


@bp_item.route('/add', methods=["GET", "POST"])
def add():
    conn = get_db()
    c = conn.cursor()

    form = NewItemForm()

    c.execute("SELECT id, name FROM category")
    categories = c.fetchall()
    form.category.choices = categories

    c.execute("SELECT id, name FROM subcategory WHERE category_id=?", (1,))
    subcategories = c.fetchall()
    form.subcategory.choices = subcategories

    if form.validate_on_submit() and form.image.validate(form, extra_validators=(FileRequired(),)):
        filename = save_image_upload(form.image)
        c.execute('''INSERT INTO item
            (title, description, price, image, category_id, subcategory_id) 
            VALUES (?,?,?,?,?,?)     
        ''', (
            form.title.data,
            form.description.data,
            float(form.price.data),
            filename,
            form.category.data,
            form.subcategory.data
        ))

        conn.commit()
        flash(f"Item {form.title.data} has been successfully submitted", "success")
        return redirect(url_for("main.index"))

    return render_template('add.html', form=form)


@bp_item.route('/<int:item_id>', methods=["GET"])
def item(item_id):
    c = get_db().cursor()
    c.execute('''SELECT
            i.id, i.title, i.description, i.price, i.image, c.name, s.name
            FROM 
            item AS i
            INNER JOIN category AS c ON i.category_id = c.id
            INNER JOIN subcategory AS s ON i.subcategory_id = s.id
            WHERE i.id = ?
        ''', (item_id,))

    row = c.fetchone()

    try:
        db_item = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'price': row[3],
            'images': row[4],
            'category_name': row[5],
            'subcategory_name': row[6],
        }
    except IndexError:
        db_item = {}

    if db_item:
        comments_from_db = c.execute('''SELECT content FROM comment
                WHERE item_id  = ? ORDER BY id DESC''', (item_id,))

        comments = [{"content": row[0]} for row in comments_from_db]

        comment_form = CommentForm()
        comment_form.item_id.data = item_id

        form = DeleteItem()
        return render_template('item.html', item=db_item, deleteForm=form, commentForm=comment_form, comments=comments)

    return redirect(url_for('main.index'))


@bp_item.route('/edit/<int:item_id>', methods=["GET", "POST"])
def edit(item_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM item WHERE id=?", (item_id,))

    row = c.fetchone()

    if row is None:
        abort(404)

    try:
        db_item = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'price': row[3],
            'images': row[4],
            'category_name': row[5],
            'subcategory_name': row[6],
        }
    except IndexError:
        db_item = {}

    if db_item:
        form = EditItem()
        if form.validate_on_submit():
            filename = db_item['images']

            if form.image.data:
                filename = save_image_upload(form.image)  # must be without data (because of save method)

            c.execute('''UPDATE item SET
            title=?, description=?, price=?, images=?
            WHERE id=?                        
            ''', (
                form.title.data,
                form.description.data,
                float(form.price.data),
                filename,
                item_id
            ))

            conn.commit()
            flash(f"Item {form.title.data} has been successfully updated", "success")
            return redirect(url_for("item.item", item_id=item_id))

        form.title.data = db_item['title']
        form.description.data = db_item['description']
        form.price.data = db_item['price']

        return render_template('update_item.html', form=form)

    abort(404)


@bp_item.route('/delete/<int:item_id>', methods=["POST"])
def delete(item_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM item WHERE id=?", (item_id,))

    row = c.fetchone()

    form = DeleteItem()
    if form.validate_on_submit():

        if row is not None:
            c.execute("DELETE FROM item WHERE id=?", (item_id,))
            conn.commit()
            flash(f"Item has been successfully deleted", "success")
        else:
            flash(f"This item does not exist", "danger")

        return redirect(url_for('main.index'))
    flash("Incorrect price", "danger")
    return redirect(url_for('item.item', item_id=item_id))
