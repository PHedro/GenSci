from django.http import HttpResponseRedirect
from django.views.generic import FormView

from patient_data.constants import XML_CONTENT_TYPE, CSV_CONTENT_TYPE
from patient_data.forms import UploadForm
from patient_data.models import BloodSample, DNASample

PARSERS = {
    XML_CONTENT_TYPE: BloodSample,
    CSV_CONTENT_TYPE: DNASample,
}


class UploadFile(FormView):
    template_name = "upload.html"
    form_class = UploadForm
    success_url = "/upload"

    def form_valid(self, form):
        uploaded_file = form.cleaned_data["file"]
        content_type = uploaded_file.content_type

        PARSERS.get(content_type).parse(uploaded_file)

        return HttpResponseRedirect(self.get_success_url())
