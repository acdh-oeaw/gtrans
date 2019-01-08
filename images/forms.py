from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Image


class GenericFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(GenericFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.add_input(Submit('Filter', 'Filter'))


class UploadZipForm(forms.Form):
    filepath = forms.CharField(label='path to file', max_length=250, required=False)
    uploaded_zip = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(UploadZipForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-1'
        self.helper.field_class = 'col-md-11'
        self.helper.add_input(Submit('submit', 'save'),)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-1'
        self.helper.field_class = 'col-md-11'
        self.helper.add_input(Submit('submit', 'save'),)
