from ambition_rando.tests import AmbitionTestCaseMixin
from ambition_subject.forms import PreviousOpportunisticInfectionForm
from ambition_subject.models import PatientHistory, PreviousOpportunisticInfection
from ambition_visit_schedule import DAY1
from django.forms import inlineformset_factory
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy


@override_settings(SITE_ID="10")
class TestSyncInlineOrder(AmbitionTestCaseMixin, TestCase):
    def setUp(self):
        screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", report_datetime=get_utcnow()
        )
        self.consent = mommy.make_recipe(
            "ambition_subject.subjectconsent",
            consent_datetime=get_utcnow(),
            screening_identifier=screening.screening_identifier,
        )

        self.appointment = Appointment.objects.get(
            visit_code=DAY1, subject_identifier=self.consent.subject_identifier
        )
        self.subject_visit = mommy.make_recipe(
            "ambition_subject.subjectvisit",
            appointment=self.appointment,
            reason=SCHEDULED,
        )

    def test_inline_order_outgoing(self):
        PatientHistoryFormSet = inlineformset_factory(
            PatientHistory,
            PreviousOpportunisticInfection,
            form=PreviousOpportunisticInfectionForm,
            extra=1,
        )
        PatientHistoryFormSet()
