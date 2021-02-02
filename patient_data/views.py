from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.generic import FormView, ListView, DetailView

from patient_data.constants import XML_CONTENT_TYPE, CSV_CONTENT_TYPE
from patient_data.forms import UploadForm, DataFilter
from patient_data.models import BloodSample, DNASample, Patient

PARSERS = {
    XML_CONTENT_TYPE: BloodSample,
    CSV_CONTENT_TYPE: DNASample,
}


class UploadFile(FormView):
    template_name = "upload.html"
    form_class = UploadForm
    success_url = "/patients"

    def form_valid(self, form):
        uploaded_file = form.cleaned_data["file"]
        content_type = uploaded_file.content_type

        PARSERS.get(content_type).parse(uploaded_file)

        return HttpResponseRedirect(self.get_success_url())


class PatientList(ListView):
    model = Patient
    allow_empty = True
    paginate_by = 30
    context_object_name = "patients_list"
    queryset = (
        Patient.objects.all()
        .order_by("identifier")
        .prefetch_related("dnasample_set", "bloodsample_set")
    )
    template_name = "patients.html"

    @never_cache
    def get(self, request, *args, **kwargs):
        data_filter = DataFilter(request.GET, queryset=self.get_queryset())
        setattr(self, "object_list", data_filter.qs)
        context = self.get_context_data()
        context.update({"filter": data_filter})
        return self.render_to_response(context)


class PatientDetail(DetailView):
    model = Patient
    queryset = Patient.objects.all().prefetch_related(
        "dnasample_set", "bloodsample_set"
    )
    context_object_name = "patient"
    template_name = "patient.html"
