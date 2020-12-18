from flask import Blueprint, render_template, send_from_directory, request

from ..forms import FilterForm
from ..helpers import uploads_path
from ..dbs.dbs import get_db

bp_main = Blueprint("main", __name__, url_prefix='/')


@bp_main.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(uploads_path, filename)


@bp_main.route('/')  # if get will be used for search it will add query in link (no "post" needed)
def index():
    conn = get_db()
    c = conn.cursor()
    # select WHAT FROM WHERE
    # to do multiple tables/columns (need to use join)
    # if we put column we should put table upfront
    # from name of column you can put only one

    form = FilterForm(request.args, meta={'csrf': False})
    # args is used to take query by request() all variable in request

    c.execute("SELECT id, name FROM category")
    categories = c.fetchall()
    categories.insert(0, (0, '---'))
    form.category.choices = categories

    c.execute("SELECT id, name FROM subcategory WHERE category_id=?", (1,))
    subcategories = c.fetchall()
    subcategories.insert(0, (0, '---'))
    form.subcategory.choices = subcategories

    query = '''SELECT
        i.id, i.title, i.description, i.price, i.image, c.name, s.name
        FROM 
        item AS i
        INNER JOIN category AS c ON i.category_id = c.id
        INNER JOIN subcategory AS s ON i.subcategory_id = s.id
    '''

    filter_queries = []
    parameters = []

    if form.title.data.strip():
        filter_queries.append('i.title LIKE ?')
        parameters.append(f'%{form.title.data.strip()}%')  # it will find any sting that contain form file data

    if form.category.data:
        filter_queries.append('i.category_id = ?')
        parameters.append(form.category.data)

    if form.subcategory.data:
        filter_queries.append('i.subcategory_id = ?')
        parameters.append(form.subcategory.data)

    if filter_queries:
        query += ' WHERE '
        query += ' AND '.join(filter_queries)

    if form.price.data:
        if form.price.data == 1:
            query += ' ORDER BY i.price DESC'
        else:
            query += ' ORDER BY i.price'  # ASC jest domyślne

    else:
        query += ' ORDER BY i.id DESC'  # newest to oldest because of id

    item_from_db = c.execute(query, tuple(parameters))

    items = []
    for row in item_from_db:
        item = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'price': row[3],
            'image': row[4],
            'category_name': row[5],
            'subcategory_name': row[6],
        }
        items.append(item)

    return render_template('index.html', items=items, form=form)
