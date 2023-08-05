from ambition_rando.constants import CONTROL, SINGLE_DOSE
from ambition_rando.models.randomization_list import RandomizationList
from ambition_rando.tests import AmbitionTestCaseMixin
from ambition_sites import fqdn, ambition_sites, get_site_id
from ambition_visit_schedule import DAY1, DAY3, DAY5
from arrow.arrow import Arrow
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_base.sites.utils import add_or_update_django_sites
from edc_reference import LongitudinalRefset
from edc_reference.tests import ReferenceTestHelper

from ..predicates import Predicates


class TestPredicates(AmbitionTestCaseMixin, TestCase):

    app_label = 'ambition_subject'
    import_randomization_list = True
    reference_helper_cls = ReferenceTestHelper
    reference_model = 'edc_reference.reference'
    visit_model = 'ambition_subject.subjectvisit'

    @classmethod
    def setUpClass(cls):
        add_or_update_django_sites(
            apps=django_apps, sites=ambition_sites, fqdn=fqdn)
        return super().setUpClass()

    def tearDown(self):
        super().tearDown()

    def update_randomization_list(self, arm):
        site = Site.objects.get_current()
        RandomizationList.objects.update(
            site_name=site.name,
            subject_identifier=None)
        rando = RandomizationList.objects.filter(
            site_name=site.name, drug_assignment=arm).order_by('sid').first()
        rando.subject_identifier = self.subject_identifier
        rando.save()

    def setUp(self):
        self.subject_identifier = '111111111'
        self.reference_helper = self.reference_helper_cls(
            visit_model=self.visit_model,
            subject_identifier=self.subject_identifier)

        report_datetime = Arrow.fromdatetime(
            datetime(2017, 7, 7)).datetime
        self.reference_helper.create_visit(
            report_datetime=report_datetime, timepoint=DAY1)
        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=3),
            timepoint=DAY3)
        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=5),
            timepoint=DAY5)

    @property
    def subject_visits(self):
        return LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model=self.visit_model,
            name=self.visit_model,
            reference_model_cls=self.reference_model
        ).order_by('report_datetime')

    def test_cd4_requisition_required(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.patienthistory',
            visit_code=self.subject_visits[0].visit_code,
            cd4_date=(self.subject_visits[0].report_datetime - relativedelta(months=4)).date())
        self.assertTrue(pc.func_require_cd4(self.subject_visits[0]))

    def test_cd4_requisition_not_required(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.patienthistory',
            visit_code=self.subject_visits[0].visit_code,
            cd4_date=(self.subject_visits[0].report_datetime).date())
        self.assertFalse(pc.func_require_cd4(self.subject_visits[0]))

    def test_vl_requisition_required(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.patienthistory',
            visit_code=self.subject_visits[0].visit_code,
            viral_load_date=(
                self.subject_visits[0].report_datetime - relativedelta(months=4)).date())
        self.assertTrue(pc.func_require_vl(self.subject_visits[0]))

    def test_vl_requisition_not_required(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.patienthistory',
            visit_code=self.subject_visits[0].visit_code,
            viral_load_date=(self.subject_visits[0].report_datetime).date())
        self.assertFalse(pc.func_require_vl(self.subject_visits[0]))

    @override_settings(SITE_ID=get_site_id('blantyre'))
    def test_pkpd_site_eq_blantyre(self):
        pc = Predicates()
        self.update_randomization_list(CONTROL)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))
        self.update_randomization_list(SINGLE_DOSE)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))

    @override_settings(SITE_ID=get_site_id('harare'))
    def test_pkpd_site_eq_harare(self):
        pc = Predicates()
        self.update_randomization_list(CONTROL)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))
        self.update_randomization_list(SINGLE_DOSE)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))

    @override_settings(SITE_ID=get_site_id('gaborone'))
    def test_pkpd_site_eq_gaborone(self):
        pc = Predicates()
        self.update_randomization_list(CONTROL)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))
        self.update_randomization_list(SINGLE_DOSE)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))

    @override_settings(SITE_ID=get_site_id('capetown'))
    def test_pkpd_site_eq_capetown(self):
        pc = Predicates()
        self.update_randomization_list(CONTROL)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))
        self.update_randomization_list(SINGLE_DOSE)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))

    @override_settings(SITE_ID=get_site_id('lilongwe'))
    def test_pkpd_site_eq_lilongwe(self):
        pc = Predicates()
        self.update_randomization_list(CONTROL)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))
        self.update_randomization_list(SINGLE_DOSE)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))

    @override_settings(SITE_ID=get_site_id('kampala'))
    def test_pkpd_site_eq_kampala(self):
        pc = Predicates()
        self.update_randomization_list(CONTROL)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))
        self.update_randomization_list(SINGLE_DOSE)
        self.assertFalse(pc.func_require_pkpd_stopcm(self.subject_visits[0]))

    @override_settings(SITE_ID=get_site_id('gaborone'))
    def test_qpcr_requisition_site_eq_gaborone(self):
        pc = Predicates()
        self.update_randomization_list(CONTROL)
        self.assertTrue(
            pc.func_require_qpcr_requisition(self.subject_visits[0]))
        self.update_randomization_list(SINGLE_DOSE)
        self.assertTrue(
            pc.func_require_qpcr_requisition(self.subject_visits[0]))

    @override_settings(SITE_ID=get_site_id('harare'))
    def test_qpcr_requisition_site_eq_harare(self):
        pc = Predicates()
        self.update_randomization_list(CONTROL)
        self.assertFalse(
            pc.func_require_qpcr_requisition(self.subject_visits[0]))
        self.update_randomization_list(SINGLE_DOSE)
        self.assertFalse(
            pc.func_require_qpcr_requisition(self.subject_visits[0]))

    @override_settings(SITE_ID=get_site_id('capetown'))
    def test_qpcr_24_requisition_site_eq_cape_town(self):
        pc = Predicates()
        self.update_randomization_list(CONTROL)
        self.assertFalse(
            pc.func_require_qpcr_requisition(self.subject_visits[0]))
        self.update_randomization_list(SINGLE_DOSE)
        self.assertFalse(
            pc.func_require_qpcr_requisition(self.subject_visits[0]))
