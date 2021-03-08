from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm


class CrispyModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrispyModelForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))


def get_dynamic_model_form(dynamic_model):
    """
    Return a form class based on dynamic_model
    """

    class DynamicModelForm(CrispyModelForm):
        class Meta:
            model = dynamic_model
            fields = "__all__"

    return DynamicModelForm
