import aiohttp
import asyncio
import async_timeout

from .cta_transit_exceptions import CTATransitAPIError


class CTATransitTracker():
    def __init__(self, session, loop):
        self._session = session
        self._loop = loop
        self.response = {}


class BusTracker(CTATransitTracker):
    def __init__(self, session, loop, api_key, response_format='json', locale='en'):
        self._api_key = api_key
        self._format = response_format
        self._locale = locale

        super().__init__(session, loop)

    async def get_time(self):
        """Get a dictionary object containing a response from the CTA Bus Tracker API gettime endpoint"""

        endpoint = 'gettime'
        params = {}
        
        self.response = await self._make_bus_api_call(endpoint, params)

    async def get_vehicles(self, vid=None, rt=None, tmres=None):
        """Get a dictionary object containing a response from the CTA Bus Tracker API getvehicles endpoint

        Keyword arguments:
        vid -- string or list of strings representing vehicle IDs.  Required.  Default None.  Raises exception if provided with non None rt parameter
        rt -- string or list of strings representing route designators.  Required.  Default None.  Raises exception if provided with non None vid parameter
        tmres -- string representing resolution of time stamps.  Optional.  Default None
        """

        endpoint = 'getvehicles'
        params = {}

        if vid is None and rt is None:
            # get_vehicles function requires one of either vid or rt to be provided
            raise CTATransitAPIError('The get_vehicles() function requires one of either vid or rt to be provided')
        if vid is not None and rt is not None:
            # Vid is not available with rt parameter and vice versa
            raise CTATransitAPIError('Vid is not available with rt parameter and vice versa')

        if vid is not None:
            params['vid'] = vid
        if rt is not None:
            params['rt'] = rt
        if tmres is not None:
            params['tmres'] = tmres

        self.response = await self._make_bus_api_call(endpoint, params)

    async def get_routes(self):
        """Get a dictionary object containing a response from the CTA Bus Tracker API getroutes endpoint"""

        endpoint = 'getroutes'
        params = {}

        return await self._make_bus_api_call(endpoint, params)

    async def get_directions(self, rt):
        """Get a dictionary object containing a response from the CTA Bus Tracker API getdirections endpoint
        
        Parameters:
        rt -- string representing a route designator
        """

        endpoint = 'getdirections'
        params = {'rt': rt}

        self.response = await self._make_bus_api_call(endpoint, params)

    async def get_stops(self, rt, dir):
        """Get a dictionary object containing a response from the CTA Bus Tracker API getstops endpoint

        Parameters:
        rt -- string representing a route designator
        dir -- string representing a route direction
        """
        endpoint = 'getstops'
        params = {'rt': rt, 'dir': dir}

        self.response = await self._make_bus_api_call(endpoint, params)

    async def get_patterns(self, pid=None, rt=None):
        """Get a dictionary object containing a response from the CTA Bus Tracker API getpatterns endpoint

        Keyword Arguments:
        pid -- string or list of strings representing pattern ids.  Required.  Default None.  Raises exception if provided with non None rt parameter
        rt -- string representing a route designator.  Required.  Default None.  Raises exception if provided with non None pid parameter
        """
        endpoint = 'getpatterns'
        params = {}

        if pid is None and rt is None:
            # Function requires one of either pid or rt to be provided
            raise CTATransitAPIError('The get_patterns() function requires one of either pid or rt to be provided')
        if pid is not None and rt is not None:
            # Pid is not available with rt parameter and vice versa
            raise CTATransitAPIError('Pid is not available with rt parameter and vice versa')

        if pid is not None:
            params['pid'] = pid
        if rt is not None:
            params['rt'] = rt

        self.response = await self._make_bus_api_call(endpoint, params)

    async def get_predictions(self, stpid=None, rt=None, vid=None, top=None):
        """Get a dictionary object containing a response from the CTA Bus Tracker API getpredictions endpoint

        Keyword Arguments:
        stpid -- string or list of strings representing stop ids.  Required.  Default None.  Raises exception if provided with non None vid parameter
        rt -- string or list of strings representing route designators.  Optional.  Default None.  Raises exception if provided with None stpid parameter
        vid -- string or list of strings representing vehicle ids.  Required.  Default None.  Raises exception if provided with non None stpid parameter
        top -- integer representing maximum predictions to be returned.  Optional.  Default None
        """
        endpoint = 'getpredictions'
        params = {}

        if stpid is None and vid is None:
            # Function requires one of either stpid or vid to be provided
            raise CTATransitAPIError('The get_predictions() function requires one of either stpid or vid to be provided')
        if stpid is not None and vid is not None:
            # Stpid not available with vid parameter and vice versa
            raise CTATransitAPIError('Stpid is not available with vid parameter and vice versa')
        if rt is not None and stpid is None:
            # Optional parameter rt only available with stpid parameter
            raise CTATransitAPIError('Rt parameter is only available with stpid parameter')
        
        if stpid is not None:
            params['stpid'] = stpid
        if rt is not None:
            params['rt'] = rt
        if vid is not None:
            params['vid'] = vid
        if top is not None:
            params['top'] = top

        self.response = await self._make_bus_api_call(endpoint, params)

    async def get_service_bulletins(self, rt=None, rtdir=None, stpid=None):
        """Get a dictionary object containing a response from the CTA Bus Tracker API getservicebulletins endpoint

        Keyword Arguments:
        rt -- string or list of strings representing route designators.  Required.  Default None
        rtdir -- string representing route direction.  Optional.  Default None
        stpid -- string or list of strings representing stop ids.  Required.  Default None
        """
        endpoint = 'getservicebulletins'
        params = {}

        if rt is None and stpid is None:
            # Function requires one of either rt or stpid to be provided
            raise CTATransitAPIError('The get_bulletins() function requires one of either rt or stpid to be provided')
        if rtdir is not None and rt is None:
            # Optional parameter rtdir only available with rt parameter
            raise CTATransitAPIError('Rtdir parameter is only available with rt parameter')

        if rt is not None:
            params['rt'] = rt
        if rtdir is not None:
            params['rtdir'] = rtdir
        if stpid is not None:
            params['stpid'] = stpid

        self.response = await self._make_bus_api_call(endpoint, params)

    async def _make_bus_api_call(self, endpoint, params, version='v2'):
        """Make an http get request to the specified endpoint of the CTA Bus Tracker API and return the response json content

        Parameters:
        endpoint -- string representing the desired api endpoint
        params -- dictionary containing the query parameters to be added to the request
        Keyword Arguments:
        version -- string representing the API version to be used.  Optional.  Default 'v2'
        """
        base_url = 'http://www.ctabustracker.com/bustime/api/{version}/{endpoint}'.format(endpoint=endpoint, version=version)

        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(url=base_url, params={'key': self._api_key, 'format': self._format, 'locale': self._locale, **params})
        except asyncio.TimeoutError:
            pass
        except aiohttp.ClientError:
            pass

        return await response.json()


class TrainTracker(CTATransitTracker):
    def __init__(self, session, loop, api_key, format_as_json=True):
        self._api_key = api_key

        if format_as_json:
            self._base_parameters = {'key': self._api_key, 'outputType': 'JSON'}
        else:
            self._base_parameters = {'key': self._api_key}

        super().__init__(session, loop)

    async def get_arrivals(self, mapid=None, stpid=None, max=None, rt=None):
        endpoint = 'ttarrivals.aspx'
        params = {}

        if mapid is None and stpid is None:
            # Function requires one of either mapid or stpid to be provided
            pass
        if mapid is not None and stpid is not None:
            # Mapid not available with stpid parameter and vice versa
            pass
        
        if mapid is not None:
            params['mapid'] = mapid
        if stpid is not None:
            params['stpid'] = stpid
        if max is not None:
            params['max'] = max
        if rt is not None:
            params['rt'] = rt

        self.response = await self._make_train_api_call(endpoint, params)

    async def get_follow_this_train(self, runnumber):
        endpoint = 'ttfollow.aspx'
        params = {'runnumber': runnumber}

        return await self._make_train_api_call(endpoint, params)

    async def get_locations(self, rt):
        endpoint = 'ttpositions.aspx'
        params = {'rt': rt}

        return await self._make_train_api_call(endpoint, params)

    async def _make_train_api_call(self, endpoint, params, version='1.0'):
        base_url = 'http://lapi.transitchicago.com/api/{version}/{endpoint}'.format(endpoint=endpoint, version=version)

        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(url=base_url, params={**self._base_parameters, **params})
        except asyncio.TimeoutError:
            pass
        except aiohttp.ClientError:
            pass

        return await response.json()
