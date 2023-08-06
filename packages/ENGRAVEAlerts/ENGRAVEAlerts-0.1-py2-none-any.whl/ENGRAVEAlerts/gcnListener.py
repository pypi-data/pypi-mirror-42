#!/usr/local/bin/python
# encoding: utf-8
"""
*Listen to GCN LV Alerts*

:Author:
    David Young

:Date Created:
    March  3, 2019
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
import gcn
from ENGRAVEAlerts import sms
import lxml.etree
from datetime import datetime
import requests
# THE LVC-GCN HANDLER
try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO
import unicodecsv as csv


class gcnListener():
    """
    *The worker class for the gcnListener module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``test`` -- use test settings for development purposes

    **Usage:**

        To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_). 

        To initiate a gcnListener object, use the following:

        .. todo::

            - add usage info
            - create a sublime snippet for usage
            - create cl-util for this class
            - add a tutorial about ``gcnListener`` to documentation
            - create a blog post about what ``gcnListener`` does

        .. code-block:: python 

            usage code   
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

    def __init__(
            self,
            log,
            settings=False,
            test=False
    ):
        self.log = log
        log.debug("instansiating a new 'gcnListener' object")
        self.settings = settings
        self.eventCache = []
        self.contacts = []
        self.test = test

        # Initial Actions
        self.cache_alert_contacts()

        return None

    def listen(
            self,
            testEventPacket=False):
        """*listen*

        **Key Arguments:**
            - ``testEventPacket`` -- use a local VOEvent Packet to test the process_gcn function

        **Return:**
            - None

        **Usage:**
            ..  todo::

                - add usage info
                - create a sublime snippet for usage
                - write a command-line tool for this method
                - update package tutorial with command-line tool info if needed

            .. code-block:: python 

                usage code 

        """
        self.log.debug('starting the ``listen`` method')

        @gcn.handlers.include_notice_types(
            gcn.notice_types.LVC_PRELIMINARY,
            gcn.notice_types.LVC_INITIAL,
            gcn.notice_types.LVC_UPDATE,
            gcn.notice_types.LVC_RETRACTION)
        def process_gcn(payload, root):

            smsContent = ""

            # DECIDE HOW TO RESPOND FOR REAL/TEST EVENTS
            if root.attrib['role'] == 'observation':
                pass
            if root.attrib['role'] == 'test':
                smsContent = "TEST ALERT: "
                if not self.test:
                    return

            # READ ALL OF THE VOEVENT PARAMETERS FROM THE "WHAT" SECTION.
            params = {elem.attrib['name']:
                      elem.attrib['value']
                      for elem in root.iterfind('.//Param')}

            try:
                # REDUCE CHARACTERS OF FAR STRING
                FARlist = params["FAR"].split("e")
                FAR = "%2.2f" % (float(FARlist[0]),)
                FAR = FAR + "e" + FARlist[1]
                params["FAR"] = FAR
            except:
                pass

            eventTime = "?"
            for elem in root.iterfind('.//ISOTime'):
                eventTime = elem.text
                try:
                    eventTime = datetime.strptime(
                        eventTime, '%Y-%m-%dT%H:%M:%S.%f')
                    eventTime = eventTime.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    print "Could not convert time stamp"
                    pass
                eventTime = eventTime + " UT"
            params["eventTime"] = eventTime

            # BUILD ALERT CONTENT
            smsContent += "%(AlertType)s notice for %(GraceID)s, a %(Group)s event detected at %(eventTime)s. FAR = %(FAR)s Hz. " % params

            if params["Group"] == "CBC":
                smsContent += "HasNS = %(HasNS)s. HasRemnant = %(HasRemnant)s. " % params

            try:
                smsContent += "%(EventPage)s" % params
            except:
                pass

            # PRINT ALL PARAMETERS.
            for key, value in params.items():
                print key, ':', value

            if params["GraceID"] not in self.eventCache:
                try:
                    self.cache_alert_contacts()
                except:
                    pass
                alerts = sms(
                    log=self.log,
                    settings=self.settings
                )
                alerts.set_mobile_numbers(self.contacts)
                alerts.send_message(smsContent)

            self.eventCache.append(params["GraceID"])

        if not testEventPacket:
            gcn.listen(handler=process_gcn)
        else:
            payload = open(testEventPacket, 'rb').read()
            root = lxml.etree.fromstring(payload)
            process_gcn(payload, root)

        self.log.debug('completed the ``listen`` method')
        return None

    def cache_alert_contacts(
            self):
        """*Download a copy of the alert contacts from google sheet*

        **Return:**
            - None

        **Usage:**
            ..  todo::

                - add usage info
                - create a sublime snippet for usage
                - write a command-line tool for this method
                - update package tutorial with command-line tool info if needed

            .. code-block:: python 

                usage code 

        """
        self.log.debug('starting the ``cache_alert_contacts`` method')

        if self.test:
            url = self.settings["contact_sheet"]["development"]
        else:
            url = self.settings["contact_sheet"]["production"]

        content = False
        try:
            response = requests.get(
                url=url,
            )
            content = response.content
            status_code = response.status_code
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

        if content:
            f = StringIO(content)
            csvReader = csv.DictReader(
                f, dialect='excel', delimiter=',', quotechar='"')
            self.contacts = []
            for row in csvReader:
                if row["SMS Alerts"] == "TRUE":
                    self.contacts.append(row["Mobile (with country code)"])
            print self.contacts

        self.log.debug('completed the ``cache_alert_contacts`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx
