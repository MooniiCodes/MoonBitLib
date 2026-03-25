import urllib.request
import json
import http.cookiejar

class MoonBitClient:
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url.rstrip('/')
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))
        self.username = username
        self.user_id = None
        
        if username and password:
            self.login(username, password)
    
    def login(self, username, password):
        """Authenticate with the server"""
        url = f"{self.base_url}/api/auth/login"
        data = {"username": username, "password": password}
        
        try:
            json_data = json.dumps(data)
            post_data = json_data.encode('utf-8')
            headers = {'Content-Type': 'application/json'}
            
            req = urllib.request.Request(url, post_data, headers)
            response = self.opener.open(req)
            result = json.loads(response.read().decode('utf-8'))
            self.user_id = result.get('uid')
            self.username = result.get('username')
            return result
        except urllib.error.HTTPError as e:
            print(f"Login failed - HTTP Error: {e.code} {e.reason}")
            raise
        except urllib.error.URLError as e:
            print(f"Login failed - URL Error: {e.reason}")
            raise
    
    def transfer(self, to_user, amount, from_user=None):
        """Transfer mBit to another user"""
        url = f"{self.base_url}/api/transfer"
        data = {
            "to": to_user,
            "amount": amount,
        }

        if from_user is not None:
            data["from"] = from_user
        elif self.user_id is not None:
            data["from"] = self.user_id
        elif self.username is not None:
            data["from"] = self.username


        
        try:
            json_data = json.dumps(data)
            post_data = json_data.encode('utf-8')
            headers = {'Content-Type': 'application/json'}
            
            req = urllib.request.Request(url, post_data, headers)
            response = self.opener.open(req)
            result = json.loads(response.read().decode('utf-8'))
            return result
        except urllib.error.HTTPError as e:
            print(f"Transfer failed - HTTP Error: {e.code} {e.reason}")
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                print(f"Server error: {error_data.get('error')}")
            except:
                pass
            raise
        except urllib.error.URLError as e:
            print(f"Transfer failed - URL Error: {e.reason}")
            raise

# Legacy function for backward compatibility
def transfer(fromuser, to, amount):
    """Legacy function - use MoonBitClient instead"""
    url = "http://136.33.83.234/api/transfer"
    data = {
        "to": to, "amount": amount, "from": fromuser
    }

    print(data)

    try:
        json_data = json.dumps(data)
        post_data = json_data.encode('utf-8')
        headers = {'Content-Type': 'application/json'}
    
        req = urllib.request.Request(url, post_data, headers)
        urllib.request.urlopen(req)

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")

