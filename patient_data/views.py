from django.http import HttpResponseRedirect
from django.views.generic import FormView

from patient_data.constants import XML_CONTENT_TYPE, CSV_CONTENT_TYPE
from patient_data.forms import UploadForm
from patient_data.parser_csv import parse as parse_csv
from patient_data.parser_xml import parse as parse_xml


PARSERS = {
    XML_CONTENT_TYPE: parse_xml,
    CSV_CONTENT_TYPE: parse_csv,
}


class UploadFile(FormView):
    template_name = "upload.html"
    form_class = UploadForm
    success_url = "/upload"

    def form_valid(self, form):
        uploaded_file = form.cleaned_data["file"]
        content_type = uploaded_file.content_type

        PARSERS.get(content_type)(uploaded_file)

        return HttpResponseRedirect(self.get_success_url())
