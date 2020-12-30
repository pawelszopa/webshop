from wtforms import ValidationError

from ..dbs.dbs import get_db


class BelongsToOtherFieldOptions:
    def __init__(self, table, belongs_to, foreign_key=None, message=None):
        if not table:
            raise AttributeError("BelongsToOtherFieldOptions validator need the table parameter")

        if not belongs_to:
            raise AttributeError("BelongsToOtherFieldOptions validator need the belongs_to parameter")

        self.table = table
        self.belongs_to = belongs_to

        if not foreign_key:
            foreign_key = belongs_to + '_id'

        if not message:
            message = 'Chosen option is not valid.'

        self.foreign_key = foreign_key
        self.message = message

    def __call__(self, form, field):
        c = get_db().cursor()
        try:
            c.execute(f"""SELECT COUNT(*) FROM {self.table} 
                WHERE id = ? AND {self.foreign_key} = ?""", (
                field.data, getattr(form, self.belongs_to).data
            ))
        except Exception as e:
            raise AttributeError(f' Passed parameters are not correct. {e}')
            #  count(*) zwraca ile jest wyników

        exists = c.fetchone()[0]
        if not exists:
            raise ValidationError(self.message)

