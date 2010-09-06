"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from datetime import datetime

from django.test import TestCase
from django.conf import settings
from ..models import *
from ..utils import EavRegistry, EavAdmin
from .models import Patient


class EavBasicTests(TestCase):


    def setUp(self):
    
        EavRegistry.unregister(Patient)
        EavRegistry.register(Patient)

        self.attribute = EavAttribute.objects.create(datatype=EavAttribute.TYPE_TEXT,
                                                name='City',
                                                help_text='The City')
        self.entity = Patient.objects.create(name="Doe")

        self.value = EavValue.objects.create(object=self.entity,
                                             attribute=self.attribute,
                                             value_text='Denver')


    def tearDown(self):
        EavRegistry.unregister(Patient)


    def test_can_create_attribute(self):
        EavAttribute.objects.create(datatype=EavAttribute.TYPE_TEXT,
                                    name='My text test',
                                    help_text='My help text')

    def test_attribute_unicode(self):
        self.assertEqual(unicode(self.attribute), "City (Text)")


    def test_can_eaventity_children_give_you_all_attributes_by_default(self):
        qs = Patient.eav.get_eav_attributes()
        self.assertEqual(list(qs), list(EavAttribute.objects.all()))


    def test_value_creation(self):
        EavValue.objects.create(object=self.entity,
                                attribute=self.attribute,
                                value_float=1.2)

    def test_value_unicode(self):
        self.assertEqual(unicode(self.value), "Doe - City: \"Denver\"")


    def test_value_unicode(self):
        self.assertEqual(unicode(self.value), "Doe - City: \"Denver\"")


    def test_value_types(self):
        _text = EavAttribute.objects.create(datatype=EavAttribute.TYPE_TEXT,
                                            name='Text',
                                            help_text='The text')
        _val = EavValue.objects.create(object=self.entity,
                                       attribute = _text)
        value = "Test text"
        _val.value = value
        _val.save()
        self.assertEqual(_val.value, value)              

        _float = EavAttribute.objects.create(datatype=EavAttribute.TYPE_FLOAT,
                                             name='Float',
                                             help_text='The float')
        _val = EavValue.objects.create(object=self.entity,
                                       attribute = _float)
        value = 1.22
        _val.value = value
        _val.save()
        self.assertEqual(_val.value, value)


        _int = EavAttribute.objects.create(datatype=EavAttribute.TYPE_INT,
                                           name='Int',
                                           help_text='The int')
        _val = EavValue.objects.create(object=self.entity,
                                       attribute = _int)
        value = 7
        _val.value = value
        _val.save()
        self.assertEqual(_val.value, value)

        _date = EavAttribute.objects.create(datatype=EavAttribute.TYPE_DATE,
                                            name='Date',
                                            help_text='The date')
        _val = EavValue.objects.create(object=self.entity,
                                       attribute = _date)
        value = datetime.now()
        _val.value = value
        _val.save()
        self.assertEqual(_val.value, value)

        _bool = EavAttribute.objects.create(datatype=EavAttribute.TYPE_BOOLEAN,
                                            name='Bool',
                                            help_text='The bool')
        _val = EavValue.objects.create(object=self.entity,
                                       attribute = _bool)
        value = False
        _val.value = value
        _val.save()
        self.assertEqual(_val.value, value)
        

    def test_eavregistry_ataches_and_detaches_eav_attribute(self):
        from ..utils import EavRegistry
        EavRegistry.unregister(Patient)
        p = Patient()
        self.assertFalse(hasattr(p, 'eav'))

        EavRegistry.register(Patient)
        p2 = Patient()
        self.assertTrue(p2.eav)


    def test_eavregistry_ataches_and_detaches_eav_attribute(self):
        from ..utils import EavRegistry
        EavRegistry.unregister(Patient)
        p = Patient()
        self.assertFalse(hasattr(p, 'eav'))

        EavRegistry.register(Patient)
        p2 = Patient()
        self.assertTrue(p2.eav)


    def test_eavregistry_accept_a_settings_class_with_get_queryset(self):
        EavRegistry.unregister(Patient)

        class PatientEav(EavAdmin):

            def get_eav_attributes(self):
                return EavAttribute.objects.all()

        EavRegistry.register(Patient, PatientEav)
        
        p = Patient()

        EavRegistry.unregister(Patient)
