import atexit
import sqlite3

from DAO import _Vaccines, _Suppliers, _Clinics, _Logistics


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def get_conn(self):
        return self._conn

    def create_tables(self):
        self._conn.executescript("""
                DROP TABLE IF EXISTS vaccines;
                CREATE TABLE vaccines(
                                    id INTEGER PRIMARY KEY,
                                    date TEXT NOT NULL,
                                    supplier INTEGER NOT NULL,
                                    quantity INTEGER NOT NULL,
                                    
                                    FOREIGN KEY (supplier) REFERENCES suppliers(id)
                                     );
                                     
                DROP TABLE IF EXISTS suppliers;      
                CREATE TABLE suppliers(
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    logistic INTEGER NOT NULL,
                                    
                                    FOREIGN KEY (logistic) REFERENCES logistics(id)                                
                                     ); 
                                     
                DROP TABLE IF EXISTS clinics; 
                CREATE TABLE clinics(
                                    id INTEGER PRIMARY KEY,
                                    location TEXT NOT NULL,
                                    demand INTEGER NOT NULL,
                                    logistic INTEGER NOT NULL,
                                    
                                    FOREIGN KEY (logistic) REFERENCES logistics(id)
                                    );
                                   
                DROP TABLE IF EXISTS logistics; 
                CREATE TABLE logistics(
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    count_sent INTEGER NOT NULL,
                                    count_received INTEGER NOT NULL
                                     );
                 """)

    def close(self):
        self._conn.commit()
        self._conn.close()


# the repository singleton
repo = _Repository()
atexit.register(repo.close)
