from markupsafe import Markup
from wtforms.fields.html5 import DecimalField
from wtforms.widgets import Input


class PriceInput(Input):
    input_type = 'number'  # type definition

    # There are  class that you can call
    # <input type="number" id="yolo" min="0" step="0.01">
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)
        kwargs.setdefault("min", "0.00")
        kwargs.setdefault("step", "0.01")

        if "value" not in kwargs:
            kwargs["value"] = field._value()
            # value is in field but as a function

        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs['required'] = True

        return Markup('''
        <div class="input-group mb-3">
        <input %s>
        <div class="input-group-append">   
        <span class="input-group-text">PLN</span>
        </div>
        
        </div>
        ''' % self.html_params(name=field.name, **kwargs))
    # prepend for move PLN to left or right but move input between div also does that
# i tak field and many other so **kwargs
# kwargs - "argumenty nazwane" are provided by dict type

#  field dzieczy po inpucie w momencie jak jest towrozoy moga być atrybuty - atrybuty sa zebrane w liste która sie nazway flags
# flags to pole obiektu field


# Markup pozawala pisać htmla w pythonie
class PriceField(DecimalField):
    widget = PriceInput()