import django.forms as forms
from .models import FileSchedularModel
import os
from urllib.parse import unquote
from django.conf import settings


class FileSchedularForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(FileSchedularForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['file_field'].required = False
        self.fields['url_field'].required = False
        self.fields['text_field'].required = False
        self.fields['text_field'].widget = forms.Textarea(attrs={'style': "width:20%%;"})

    class Meta:
        model = FileSchedularModel
        fields = ["file_field","url_field","text_field"]

        labels = {
            'file_field': ('Add a file'),
            'url_field':('Add a url to attach to this tweet'),
            'text_field':('Type raw tweet or tag someone')
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
                os.rename(settings.MEDIA_ROOT+"/documents/"+file_field.name,settings.MEDIA_ROOT+"/documents/"+getFilename(file_field.name)+".mp4")
                cleaned_data["file_field"] = open(settings.MEDIA_ROOT+"/documents/"+getFilename(file_field.name)+".mp4","rb")

            if not (file_field.name.endswith(".jpg") or file_field.name.endswith(".jpeg") or file_field.name.endswith(".png") or file_field.name.endswith(".mp4")):
                error = "Valid formats are .jpg, .jpeg, .png, .mp4, .mov"
                field = "file_field"
                self.add_error(field,error)
                raise forms.ValidationError(error)
        return self.cleaned_data

def getFilename(name):
    return os.path.splitext(name)[0]
