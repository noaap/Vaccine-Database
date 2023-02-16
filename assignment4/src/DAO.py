from DTO import Vaccine, Supplier, Clinic, Logistic


class _Vaccines:

    def __init__(self, conn):
        self._conn = conn
        self.counter = 0
        self.amount = 0

    def insert(self, vaccineDTO):
        self._conn.execute("""
        INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?,?, ?, ?)
        """, [vaccineDTO.id, vaccineDTO.date, vaccineDTO.supplier, vaccineDTO.quantity])
        self.counter = self.counter + 1
        self.amount += int(vaccineDTO.quantity)

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM vaccines WHERE id = ?
        """, [vaccine_id])

        return Vaccine(*c.fetchone())

    def get_counter(self):
        return self.counter


class _Suppliers:

    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplierDTO):
        self._conn.execute("""
             INSERT INTO suppliers (id, name, logistic) VALUES (?,?,?)
             """, [supplierDTO.id, supplierDTO.name, supplierDTO.logistic])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM suppliers WHERE id = ?
        """, [supplier_id])

        return Supplier(*c.fetchone())

    def find_by_name(self, supplier_name):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM suppliers WHERE name = ?
        """, [supplier_name])

        return Supplier(*c.fetchone())


class _Clinics:

    def __init__(self, conn):
        self._conn = conn
        self.demand = 0

    def insert(self, clinicDTO):
        self._conn.execute("""
        INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
        """, [clinicDTO.id, clinicDTO.location, clinicDTO.demand, clinicDTO.logistic])
        self.demand += int(clinicDTO.demand)

    def find(self, clinic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM clinics WHERE id = ?
        """, [clinic_id])

        return Clinic(*c.fetchone())

    def find_by_location(self, clinic_location):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM clinics WHERE location = ?
        """, [clinic_location])

        return Clinic(*c.fetchone())

    def change_demand(self, clinic_id, demand):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM clinics WHERE id = ?
            """, [clinic_id])
        current_demand = Clinic(*c.fetchone()).demand
        updated_demand = current_demand - demand
        if updated_demand < 0:
            updated_demand = 0
        c.execute("""
                UPDATE clinics SET demand = ? WHERE id = ?
                    """, [updated_demand, clinic_id])

        if self.demand - demand <= 0:
            self.demand = 0
        else:
            self.demand = self.demand - demand



class _Logistics:

    def __init__(self, conn):
        self._conn = conn

    def insert(self, logisticDTO):
        self._conn.execute("""
        INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
        """, [logisticDTO.id, logisticDTO.name, logisticDTO.count_sent, logisticDTO.count_received])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM logistics WHERE id = ?
        """, [logistic_id])

        return Logistic(*c.fetchone())

    def update_sent(self, logisticDTO, amount_sent):
        c = self._conn.cursor()

        c.execute("""
                        UPDATE logistics SET count_sent = ? WHERE id = ?
                            """, [logisticDTO.count_sent + amount_sent, logisticDTO.id])

    def update_received(self, logisticDTO, amount_received):
        c = self._conn.cursor()

        c.execute("""
                        UPDATE logistics SET count_received = ? WHERE id = ?
                            """, [logisticDTO.count_received + amount_received, logisticDTO.id])

