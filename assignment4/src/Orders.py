import string

from Repository import repo
import os
import DTO
from Repository import repo


class Orders:
    def __init__(self, orders_path, output_path):
        self.output_file_path = output_path
        self.orders_file_path = orders_path
        self.total_received = 0
        self.total_sent = 0

    def run(self):
        file = open(self.output_file_path, 'r+')
        file.truncate(0)
        # cleaning the output file.
        with open(self.orders_file_path, "r") as orders_file:
            for line in orders_file:
                line = line.strip()
                line = line.split(",")
                if len(line) == 3:  # we got a shipment
                    self.receive_shipment(line)
                else:  # len = 2: we need to send a shipment
                    self.send_shipment(line)

    def receive_shipment(self, line):
        name = line[0]
        amount = int(line[1])
        date = line[2]
        supplier_id = repo.suppliers.find_by_name(name)  # getting the supplier id by its name.
        # increasing the number if count_received
        logistic = supplier_id.logistic
        logistic = repo.logistics.find(logistic)
        repo.logistics.update_received(logistic,amount)
        supplier_id = supplier_id.id
        vaccine_id = repo.vaccines.get_counter() + 1
        vaccine = DTO.Vaccine(vaccine_id, date, supplier_id, amount)
        repo.vaccines.insert(vaccine)
        self.total_received = self.total_received + amount
        with open(self.output_file_path, "a") as output_file:
            summary_line = str(repo.vaccines.amount) + "," + str(repo.clinics.demand) + "," + str(
                self.total_received) + "," + str(self.total_sent) + '\n'
            output_file.write(summary_line)

    def send_shipment(self, line):
        location = line[0]
        demand = int(line[1])
        self.total_sent = self.total_sent + demand

        clinic = repo.clinics.find_by_location(location)
        logistic = repo.logistics.find(clinic.logistic)
        # increasing the amount sent
        repo.logistics.update_sent(logistic, demand)
        repo.clinics.change_demand(clinic.id, demand)
        repo.vaccines.amount = repo.vaccines.amount - demand

        with open(self.output_file_path, "a") as output_file:
            summary_line = str(repo.vaccines.amount) + "," + str(repo.clinics.demand) + "," + str(
                self.total_received) + "," + str(self.total_sent) + '\n'
            output_file.write(summary_line)
