from django.forms import ModelForm
from .models import InstaFileSchedular
import os
from urllib.parse import unquote
from django.conf import settings
import django.forms as forms
from PIL import Image
import io


class InstaFileSchedularForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(InstaFileSchedularForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['file_field'].required = True
        self.fields['text_field'].required = False
        self.fields['text_field'].widget = forms.Textarea(attrs={'style': "width:20%%;"})


    class Meta:
        model = InstaFileSchedular
        fields = ["file_field","text_field"]
        labels = {
            'file_field': ('Add a file'),
            'text_field':('Type caption')
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("file_field") == None and cleaned_data.get("text_field")=="":
            error = "Fill atleast one field"

            raise forms.ValidationError(error)
        file_field = cleaned_data.get("file_field")
        if file_field:

            file_field.name = file_field.name.replace("%20","")
            file_field.name = file_field.name.replace(",","")

            if file_field.name.endswith(".PNG") or file_field.name.endswith(".png"):
                file_field.name = getFilename(file_field.name)+".jpeg"

            if not (file_field.name.endswith(".jpg") or file_field.name.endswith(".jpeg") or file_field.name.endswith(".JPG") or file_field.name.endswith(".JPEG")):
                error = "Valid extensions are .jpg, .jpeg, .png"
                field = "file_field"
                self.add_error(field,error)
                raise forms.ValidationError(error)



        return self.cleaned_data
def getFilename(name):
    return os.path.splitext(name)[0]
