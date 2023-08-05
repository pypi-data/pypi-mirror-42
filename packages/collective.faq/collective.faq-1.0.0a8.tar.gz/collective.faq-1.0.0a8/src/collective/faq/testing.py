# -*- coding: utf-8 -*-
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import collective.faq


class CollectivefaqCoreLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.faq)

    def setUpPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        api.content.create(
            type='Document',
            id='front-page',
            title='Welcome',
            container=portal
        )
        logout()
        applyProfile(portal, 'collective.faq:default')


COLLECTIVEFAQ_CORE_FIXTURE = CollectivefaqCoreLayer()


COLLECTIVEFAQ_CORE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVEFAQ_CORE_FIXTURE,),
    name='CollectivefaqCoreLayer:IntegrationTesting'
)


COLLECTIVEFAQ_CORE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVEFAQ_CORE_FIXTURE, z2.ZSERVER_FIXTURE),
    name='CollectivefaqCoreLayer:FunctionalTesting'
)


COLLECTIVEFAQ_CORE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVEFAQ_CORE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectivefaqCoreLayer:AcceptanceTesting'
)
