import requests
import json

name = "nwebclient"

class NWebGroup:
    __client = None
    __data = None
    def __init__(self, client, data):
        self.__client = client
        self.__data = data
    def guid():
        return self.__data['guid']
    def title():
        return self.__data['title']
    def println(self):
        for key, value in self.__data.iteritems():
            print key + ": " + value
    def asDict(self):
        return self.__data;
    def docs(self):
        """ 
        :rtype: [NWebDoc]
        """
        contents = self.__client.req('api/documents/' + self.__data['group_id'])
        j =json.loads(contents);
        items = j['items'];
        #return j.items;
        return map(lambda x: NWebDoc(self.__client, x), items)
class NWebDoc:
    __client = None
    __data = None
    def __init__(self, client, data):
        self.__client = client
        self.__data = data
    def title(self):
        return self.__data['title']
    def name(self):
        return self.__data['name']
    def kind(self):
        return self.__data['kind']
    def content(self):
        return self.__data['content']
    def printInfo(self):
        s = "Doc-"+self.kind()+"(id:"+self.id()+", title: "+self.title()
        if (self.kind()=="image"):
            s+=" thumb: " + self.__data['thumbnail']['nn'] + " "
        s+=")"
        print s
    def id(self):
        return self.__data['document_id']    
    def tags(self):
        return self.__data['tags']
    def println(self):
        print self.__data
        #for key, value in self.__data.iteritems():
        #    print key + ": " + value
    def downloadThumbnail(self, size = 'nn'):
        # TODO imple
        return 0
    def setContent(self, content):
        self.__data['content'] = content
        self.__client.req('api/document/'+self.__data['document_id'], {
            'action': 'update',
            'content': content
        })
class NWebClient:
    __url = ""
    __user = ""
    __pass = ""
    def __init__(self, url, username = "", password = ""):
        """ Anstatt url kann auch ein Pfad zur einer JSON-Datei, die die Schluessel enthaelt, angegeben werden. """
        if (url[0] is '/'):
            j = json.loads(file_get_contents("/nweb.json"))
            self.__url = j['url']
            self.__user = j['username']
            self.__pass = j['password']
        else:
            self.__url = url
            self.__user = username
            self.__pass = password
    def file_get_contents(filename):
        with open(filename) as f:
            return f.read()
    def req(self, path, params = {}):
        if self.__user != "":
            params["username"]= self.__user
            params["password"]= self.__pass
        res = requests.post(self.__url+path, data=params)
        return res.text
    def doc(self, id):
        data = json.loads(self.req("api/document/"+id, {format:"json"}));
        return NWebDoc(self, data)
    def group(self, id): 
        data = json.loads(self.req("api/group/"+id, {format:"json"}))
        return NWebGroup(self, data)
    def getOrCreateGroup(self, guid, title):
        return "TODO"
