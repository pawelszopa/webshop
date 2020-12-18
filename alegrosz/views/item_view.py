from flask import Blueprint, flash, url_for, render_template
from werkzeug.utils import redirect

from ..dbs.dbs import get_db
from ..forms.item_forms import NewItemForm

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

    if form.validate_on_submit():
        c.execute('''INSERT INTO item
            (title, description, price, image, category_id, subcategory_id) 
            VALUES (?,?,?,?,?,?)     
        ''', (
            form.title.data,
            form.description.data,
            float(form.price.data),
            form.image.data,
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
            'image': row[4],
            'category_name': row[5],
            'subcategory_name': row[6],
        }
    except IndexError:
        db_item = {}

    if db_item:
        return render_template('item.html', item=db_item)

