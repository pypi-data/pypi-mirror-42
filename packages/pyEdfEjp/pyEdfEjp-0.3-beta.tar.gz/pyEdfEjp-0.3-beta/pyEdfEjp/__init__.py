from datetime import datetime
import urllib.request
import json


class EdfEjp:
    """
     TODO : ADD REQUEST FOR SPECIFIC DATES, NOT ONLY FOR TODAY AND TOMORROW

    """

    URL = 'https://particulier.edf.fr/bin/edf_rc/servlets/ejptemponew?Date_a_remonter={}&TypeAlerte=EJP'
    JSON_TODAY = 'JourJ'
    JSON_TOMORROW = 'JourJ1'
    JSON_IS_EJP = 'EST_EJP'
    JSON_IS_NOT_EJP = 'NON_EJP'
    JSON_UNKONWN_EJP = 'ND'
    JSON_PREFIX_ZONE = 'Ejp'

    URL_START_EJP = 'https://particulier.edf.fr/services/rest/referentiel/getConfigProperty?PARAM_CONFIG_PROPERTY=param.date.debut.ejp'
    JSON_ARGUMENT_START_EJP = 'param.date.debut.ejp'

    URL_END_EJP = 'https://particulier.edf.fr/services/rest/referentiel/getConfigProperty?PARAM_CONFIG_PROPERTY=param.date.fin.ejp'
    JSON_ARGUMENT_END_EJP = 'param.date.fin.ejp'

    URL_TOTAL_DAYS = 'https://particulier.edf.fr/services/rest/referentiel/getConfigProperty?PARAM_CONFIG_PROPERTY=param.total.days.{}'
    JSON_ARGUMENT_TOTAL_DAYS = 'param.total.days.{}'

    URL_HISTORIC = 'https://particulier.edf.fr/services/rest/referentiel/historicEJPStore?searchType=ejp'
    JSON_ARGUMENT_DAYS_USED = 'TotalCurrentPeriod'

    OUEST = 'Ouest'
    NORD = 'Nord'
    SUD = 'Sud'
    PACA = 'Paca'

    def __init__(self, zone=OUEST):
        self.zone = zone
        self.today = None
        self.tomorrow = None
        self.start = None
        self.end = None
        #Total of EJP days already done
        self.days_used = None
        #Total of EJP days that should be in the period
        self.total_days = None

        # The update of the start, stop and total day does not change, so it's only done one time at the start
        # Update the start of the EJP Period
        data = self._get_json_from_request(self.URL_START_EJP)
        self.start = datetime.strptime(data[self.JSON_ARGUMENT_START_EJP], '%Y-%m-%d')

        # Update the end of the EJP Period
        data = self._get_json_from_request(self.URL_END_EJP)
        self.start = datetime.strptime(data[self.JSON_ARGUMENT_END_EJP], '%Y-%m-%d')

        # Update the total days of the EJP Period
        data = self._get_json_from_request(self.URL_TOTAL_DAYS.format(self.zone.lower()))
        self.total_days = int(data[self.JSON_ARGUMENT_TOTAL_DAYS.format(self.zone.lower())])

    def update(self):
        data = self._get_json_from_request(self.URL.format("2019-02-27"))
        if data[self.JSON_TODAY][self.JSON_PREFIX_ZONE + self.zone] == self.JSON_IS_EJP:
            self.today = True
        if data[self.JSON_TODAY][self.JSON_PREFIX_ZONE + self.zone] == self.JSON_IS_NOT_EJP:
            self.today = False
        if data[self.JSON_TODAY][self.JSON_PREFIX_ZONE + self.zone] == self.JSON_UNKONWN_EJP:
            self.today = None
        if data[self.JSON_TOMORROW][self.JSON_PREFIX_ZONE + self.zone] == self.JSON_IS_EJP:
            self.tomorrow = True
        if data[self.JSON_TOMORROW][self.JSON_PREFIX_ZONE + self.zone] == self.JSON_IS_NOT_EJP:
            self.tomorrow = False
        if data[self.JSON_TOMORROW][self.JSON_PREFIX_ZONE + self.zone] == self.JSON_UNKONWN_EJP:
            self.tomorrow = None

        data = self._get_json_from_request(self.URL_HISTORIC)
        self.days_used = int(data[self.zone.upper()][self.JSON_ARGUMENT_DAYS_USED])

    def is_today_ejp(self):
        return self.today

    def is_tomorrow_ejp(self):
        return self.tomorrow

    def get_days_ejp_used(self):
        return self.days_used

    def get_days_ejp_left(self):
        return self.total_days - self.days_used

    def get_total_days(self):
        return self.total_days

    def get_start_date(self):
        return self.start

    def get_end_date(self):
        return self.stop

    def get_zone(self):
        return self.zone

    def _get_json_from_request (self, url):
        req = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.read())

        r = response.read()
        return json.loads(r.decode('utf-8'))
