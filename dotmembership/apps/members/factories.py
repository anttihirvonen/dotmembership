# encoding: utf-8
import factory
import factory.fuzzy

from . import models

FIRST_NAMES = [u'Antti', u'Petteri', u'Paula', 'Markus', 'Konsta']
LAST_NAMES = ['Virtanen', 'Kinnunen', 'Hakkarainen', u'Väänänen']
TOWNS = ['Espoo', 'Helsinki', 'Joensuu', 'Vantaa']
SCHOOLS = ['Aalto', 'Aalto School of Science', 'ELEC']
MAJORS = ['Computer Science', 'tietoliikenne', 'akustiikka', 'eiolee']


class MemberFactory(factory.Factory):
    FACTORY_FOR = models.Member

    first_name = factory.fuzzy.FuzzyChoice(FIRST_NAMES)
    last_name = factory.fuzzy.FuzzyChoice(LAST_NAMES)
    # sequence to make email always unique
    email = factory.LazyAttributeSequence(lambda o, n: u'{0}.{1}{2}@example.org'.format(o.first_name, o.last_name, n))
    home_town = factory.fuzzy.FuzzyChoice(TOWNS)

    school = factory.fuzzy.FuzzyChoice(SCHOOLS)
    major = factory.fuzzy.FuzzyChoice(MAJORS)
    class_year = factory.fuzzy.FuzzyInteger(2000, 2020)

    # always normal membership type since we don't currently support
    # anything else
    membership_type = models.Member.MEMBERSHIP.normal
