# DTO:

class Vaccine:

    def __init__(self, id_num, date, supplier, quantity):
        self.id = id_num
        self.date = date
        self.supplier = supplier
        self.quantity = quantity


class Supplier:

    def __init__(self, id_num, name, logistic):
        self.id = id_num
        self.name = name
        self.logistic = logistic


class Clinic:

    def __init__(self, id_num, location, demand, logistic):
        self.id = id_num
        self.location = location
        self.demand = demand
        self.logistic = logistic


class Logistic:

    def __init__(self, id_num, name, count_sent, count_received):
        self.id = id_num
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received


