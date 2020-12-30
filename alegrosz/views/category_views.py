from flask import Blueprint, jsonify

from ..dbs.dbs import get_db

bp_category = Blueprint('category', __name__, url_prefix='/categories')


@bp_category.route('/<int:category_id>')
def category(category_id):
    c = get_db().cursor()

    c.execute("""SELECT id, name FROM subcategory
                WHERE category_id=?
                """, (category_id,))

    subcategories = c.fetchall()

    return jsonify(subcategories=subcategories)
