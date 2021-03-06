# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 13:44:20 2014

@author: CTremblay
"""
import pyhaystack.client.HaystackClient as hc
import pyhaystack.info as info
import requests
import re

class Connect(hc.Connect):
    """
    This class connects to NiagaraAX and fetch haystack servlet
    A session is open and authentication will persist
    """
    def __init__(self,url,username,password,**kwargs):
        """
        Define Niagara AX specific local variables : url
        Calls the authenticate function
        """
        hc.Connect.__init__(self,url,username,password,**kwargs)
        self.loginURL = self.baseURL + "login/"
        self.queryURL = self.baseURL + "haystack/"
        self.requestAbout = "about"
        self.authenticate()
        
    def authenticate(self):
        """
        Login to the server
        Get the cookie from the server, configure headers, make a POST request with credential informations.
        When connected, ask the haystack for "about" information and print connection information
        """
        print('pyhaystack %s | Authentication to %s' % (info.__version__,self.loginURL))
        print('Initiating connection')
        try :
            # Try to reach server before going further 
            connection_status = self.s.get(self.loginURL).status_code
        except requests.exceptions.RequestException as e:
            connection_status = 0
            
        if connection_status == 200:
            print('Initiating authentication')
            try:
                self.COOKIE = self.s.get(self.loginURL).cookies
            except requests.exceptions.RequestException as e:
                print('Problem connecting to server : %s' % e)

            if self.COOKIE:
                try:
                    self.COOKIEPOSTFIX = self.COOKIE['niagara_session']
                    self.headers = {'cookiePostfix' : self.COOKIEPOSTFIX}
                except Exception as e:
                    pass
            self.headers =  {'token':'',
                             'scheme':'cookieDigest',
                             'absPathBase':'/',
                             'content-type':'application/x-niagara-login-support',
                             'Referer':self.baseURL+'login/',
                             'accept':'application/json; charset=utf-8'
                            }
            # Authentication post request
            try:
                req = self.s.post(self.loginURL, params=self.headers,auth=(self.USERNAME, self.PASSWORD))
                #If word 'login' is in the response page, consider login failed...
                if re.search(re.compile('login', re.IGNORECASE), req.text):
                    self.isConnected = False
                    print('Connection failure, check credentials')
                else:
                    self.isConnected = True
                    print('User logged in...')                
            except requests.exceptions.RequestException as e:
                print('Request POST error : %s' % e)
        else:
            print('Connection failed, check your parameters or VPN connection...')
        
        #Continue with haystack login
        if self.isConnected:
            self.about = self.read(self.requestAbout)
            self.serverName = self.about['rows'][0]['serverName']
            self.haystackVersion = self.about['rows'][0]['haystackVersion']
            self.axVersion = self.about['rows'][0]['productVersion']
            self.timezone = 'America/' + self.read('read?filter=site')['rows'][0]['tz']
            print('Time Zone used : %s' % self.timezone)
            print('Connection succeed with haystack on %s (%s) running haystack version %s' %(self.serverName,self.axVersion,self.haystackVersion))                              
            self.refreshHisList()    
            