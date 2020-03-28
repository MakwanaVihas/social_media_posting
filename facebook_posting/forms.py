import django.forms as forms
from .models import FBFileSchedularModel
import os
from urllib.parse import unquote
from django.conf import settings

class FBFileSchedularForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor

        super(FBFileSchedularForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['file_field'].required = False
        self.fields['url_field'].required = False
        self.fields['text_field'].required = False
        self.fields['text_field'].widget = forms.Textarea(attrs={'style': "width:20%%;"})

    class Meta:
        model = FBFileSchedularModel
        fields =  ["file_field","url_field","text_field"]

        labels = {
            'file_field': ('Add a file'),
            'url_field':('Add a url to attach to this post'),
            'text_field':('Type raw post')
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("file_field") == None and cleaned_data.get("text_field")=="" and cleaned_data.get("url_field")=="":
            error = "Fill atleast one field"
            raise forms.ValidationError(error)

        file_field = cleaned_data.get("file_field")
        if file_field:

            file_field.name = file_field.name.replace("%20","")
            file_field.name = file_field.name.replace(",","")


            if file_field.name.endswith(".mov") or file_field.name.endswith(".MOV") or file_field.name.endswith(".MP4"):
                file_field.name = getFilename(file_field.name)+".mp4"

            if not (file_field.name.endswith(".jpg") or file_field.name.endswith(".jpeg") or file_field.name.endswith(".png") or file_field.name.endswith(".mp4")
                 or file_field.name.endswith(".JPG") or file_field.name.endswith(".JPEG") or file_field.name.endswith(".PNG") or file_field.name.endswith(".MP4")):
                error = "Valid formats are .jpg, .jpeg, .png, .mp4, .mov"
                field = "file_field"
                self.add_error(field,error)
                raise forms.ValidationError(error)
        return self.cleaned_data

def getFilename(name):
    return os.path.splitext(name)[0]
