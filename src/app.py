class App:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls)
            cls._instance.access_token = None
            cls._instance.refresh_token = None
        return cls._instance
    
    def set_tokens(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
    
    def get_access_token(self):
        return self.access_token
    
    def get_refresh_token(self):
        return self.refresh_token