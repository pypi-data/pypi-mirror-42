from datetime import timedelta
import logging
import os
import requests

logger = logging.getLogger('pyrepetier')

__version__ = '2.0.1'

SCAN_INTERVAL = timedelta(seconds=5)


class Repetier():
    """Repetier Server Class"""

    def __init__(self, **kwargs):
        """Init the communications"""
        url = kwargs.pop('url', None)
        port = kwargs.pop('port', 3344)
        api_key = kwargs.pop('apikey', None)
        self._baseurl = url + ':' + str(port)
        self._apikey = 'apikey=' + api_key
        self._detail = {}

    def getPrinters(self):
        """Get printer SLUG list"""
        reqUrl = self._baseurl + '/printer/list/?' + self._apikey
        response = requests.get(reqUrl)
        if response.status_code != 200:
            logger.warning("Invalid response from API")
            self._detail = {}
            self._states = {}
        else:
            data = response.json()
            data_dict = {}
            state_dict = {}
            i = 0
            for printer in data['data']:
                prn_dict = {}
                api_dict = {}
                prn_dict['id'] = i
                prn_dict['slug'] = printer['slug']
                prn_dict['name'] = printer['name']
                if printer['online'] == 0:
                    state = 'off'
                else:
                    if printer['job'] == 'none':
                        state = 'idle'
                    else:
                        state = 'printing'
                        api_dict['done'] = printer['done']
                        api_dict['job_name'] = printer['job']
                        api_dict['job_id'] = printer['jobid']
                        api_dict['analysed'] = printer['analysed']
                        api_dict['linessent'] = printer['linesSend']
                        api_dict['oflayer'] = printer['ofLayer']
                        api_dict['printtime'] = printer['printTime']
                        api_dict['printedtimecomp'] = printer['printedTimeComp']
                        api_dict['start'] = printer['start']
                        api_dict['totallines'] = printer['totalLines']
                        if printer['paused'] == True:
                            state = 'paused'
                    self.__getDetails(i, printer['slug'])
                api_dict['state'] = state
                if i not in data_dict.keys():
                    data_dict[i] = prn_dict
                    state_dict[i] = api_dict
                else:
                    data_dict[i].update(prn_dict)
                    state_dict[i].update(api_dict)
                i += 1
            self._states = state_dict
            return data_dict

    def __getDetails(self, id, slug):
        """Get detailed information on printer"""
        reqUrl = self._baseurl + '/printer/api/' + slug + '?a=stateList&' + self._apikey
        response = requests.get(reqUrl)
        if response.status_code != 200:
            logger.warning("Invalid response from API")
            self._detail = {}
            self._states = {}
        else:
            data = response.json()
            data_dict = self._detail
            detail_dict = {}
            detail_dict['activeextruder'] = data[slug]['activeExtruder']
            detail_dict['firmware'] = data[slug]['firmware']
            detail_dict['firmwareurl'] = data[slug]['firmwareURL']
            detail_dict['multiplier'] = data[slug]['flowMultiply']
            detail_dict['xhome'] = data[slug]['hasXHome']
            detail_dict['yhome'] = data[slug]['hasYHome']
            detail_dict['zhome'] = data[slug]['hasZHome']
            detail_dict['layer'] = data[slug]['layer']
            detail_dict['lights'] = data[slug]['lights']
            detail_dict['numextruder'] = data[slug]['numExtruder']
            detail_dict['recording'] = data[slug]['rec']
            detail_dict['sdcardmounted'] = data[slug]['sdcardMounted']
            detail_dict['speedmultiplier'] = data[slug]['speedMultiply']
            detail_dict['volumetric'] = data[slug]['volumetric']
            detail_dict['x'] = data[slug]['x']
            detail_dict['y'] = data[slug]['y']
            detail_dict['z'] = data[slug]['z']

            ext_dict = {}
            e = 0
            for extruder in data[slug]['extruder']:
                nozzle_dict = {}
                nozzle_dict['error'] = extruder['error']
                nozzle_dict['output'] = extruder['output']
                nozzle_dict['tempset'] = extruder['tempSet']
                nozzle_dict['temp'] = extruder['tempRead']
                if e not in ext_dict.keys():
                    ext_dict[e] = nozzle_dict
                else:
                    ext_dict[e].update(nozzle_dict)
                e += 1
            detail_dict['nozzle'] = ext_dict

            fans_dict = {}
            f = 0
            for fan in data[slug]['fans']:
                fan_dict = {}
                fan_dict['on'] = fan['on']
                fan_dict['voltage'] = fan['voltage']
                if f not in fans_dict.keys():
                    fans_dict[f] = fan_dict
                else:
                    fans_dict[f].update(fan_dict)
                f += 1
            detail_dict['fan'] = fans_dict

            beds_dict = {}
            b = 0
            for bed in data[slug]['heatedBeds']:
                bed_dict = {}
                bed_dict['error'] = bed['error']
                bed_dict['output'] = bed['output']
                bed_dict['temp'] = bed['tempRead']
                bed_dict['tempset'] = bed['tempSet']
                if b not in beds_dict.keys():
                    beds_dict[b] = bed_dict
                else:
                    beds_dict[b].update(bed_dict)
                b += 1
            detail_dict['bed'] = beds_dict

            chambers_dict = {}
            c = 0
            for chamber in data[slug]['heatedChambers']:
                chamber_dict = {}
                chamber_dict['error'] = chamber['error']
                chamber_dict['output'] = chamber['output']
                chamber_dict['temp'] = chamber['tempRead']
                chamber_dict['tempset'] = chamber['tempSet']
                if c not in chambers_dict.keys():
                    chambers_dict[c] = chamber_dict
                else:
                    chambers_dict[c].update(chamber_dict)
                c += 1
            detail_dict['chamber'] = chambers_dict

            if id not in data_dict.keys():
                data_dict[id] = detail_dict
            else:
                data_dict[id].update(detail_dict)
            self._detail = data_dict

    def Nozzle(self, id):
        """Get the current nozzle temperature"""
        try:
            return self._detail[id]['nozzle']
        except:
            return None

    def Bed(self, id):
        """Get the current bed temperature"""
        try:
            return self._detail[id]['bed']
        except:
            return None

    def ActiveExtruder(self, id):
        """Get the active extruder"""
        try:
            return self._detail[id]['activeextruder']
        except:
            return None

    def State(self, id):
        """Get the state of the printer"""
        try:
            return self._states[id]['state']
        except:
            return None

    def Percent(self, id):
        """Get percentage done"""
        try:
            return self._states[id]['done']
        except:
            return None

    def JobName(self, id):
        """Get job name"""
        try:
            return self._states[id]['job_name']
        except:
            return None

    def JobID(self, id):
        """Get job id"""
        try:
            return self._states[id]['job_id']
        except:
            return None

    def TotalLines(self, id):
        """Get total lines of gcode"""
        try:
            return self._states[id]['totallines']
        except:
            return None

    def LinesSent(self, id):
        """Get lines of gcode sent"""
        try:
            return self._states[id]['linessent']
        except:
            return None

    def TimeStart(self, id):
        """Get Print start time"""
        try:
            return self._states[id]['start']
        except:
            return None

    def PrintLength(self, id):
        """Get Print completion time"""
        try:
            return self._states[id]['printtime']
        except:
            return None

    def PrintTime(self, id):
        """Get print time"""
        try:
            return self._states[id]['printedtimecomp']
        except:
            return None

