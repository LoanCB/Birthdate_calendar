from django.forms import Widget, TextInput


class FormControlMixin(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        css_classes = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg w-full p-2.5'

        if 'class' in self.attrs:
            self.attrs['class'] += css_classes
        else:
            self.attrs['class'] = css_classes


class FormControlTextInput(FormControlMixin, TextInput):
    pass
