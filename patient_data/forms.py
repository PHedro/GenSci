from django.forms import Form, FileField


class UploadForm(Form):
    file = FileField()
