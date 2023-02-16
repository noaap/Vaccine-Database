import sys
import sqlite3
import os
import DTO
import Orders

from Repository import repo


# define connection and cursor
# args = {config.txt, orders.txt, output.txt}
def main(args):
    f = open(args[1])  # TODO: change to: f = open(args[1])
    conn = repo.get_conn()
    repo.create_tables()
    first_line = f.readline().strip()  # 1,3,5,17
    number_of_objects = first_line.split(',')
    for i in range(int(number_of_objects[0])):  # vaccines
        vaccine = f.readline().strip()
        vaccine = vaccine.split(',')
        id_num = vaccine[0]
        date = vaccine[1]
        supplier = vaccine[2]
        quantity = vaccine[3]
        vaccine = DTO.Vaccine(id_num, date, supplier, quantity)
        repo.vaccines.insert(vaccine)
    for i in range(int(number_of_objects[1])):  # suppliers
        supplier = f.readline().strip()
        supplier = supplier.split(',')
        id_num = supplier[0]
        name = supplier[1]
        logistic = supplier[2]
        supplier = DTO.Supplier(id_num, name, logistic)
        repo.suppliers.insert(supplier)
    for i in range(int(number_of_objects[2])):  # clinics
        clinic = f.readline().strip()
        clinic = clinic.split(',')
        id_num = clinic[0]
        location = clinic[1]
        demand = clinic[2]
        logistic = clinic[3]
        clinic = DTO.Clinic(id_num, location, demand, logistic)
        repo.clinics.insert(clinic)
    for i in range(int(number_of_objects[3])):  # logistics
        logistic = f.readline().strip()
        logistic = logistic.split(',')
        id_num = logistic[0]
        name = logistic[1]
        count_sent = logistic[2]
        count_received = logistic[3]
        logistic = DTO.Logistic(id_num, name, count_sent, count_received)
        repo.logistics.insert(logistic)

    conn.commit()
    orders = Orders.Orders(args[2], args[3])
    orders.run()
    conn.commit()


databaseExisted = os.path.isfile('database.db')

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

if __name__ == '__main__':
    main(sys.argv)
