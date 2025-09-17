import csv
import pandas as pd
import os


def reads_financial_transactions(file_path):
    """считывает файл csv, выводит в виде списка словарей"""
    with open(file_path, "r", encoding="UTF-8") as file:
        reader = csv.DictReader(file)
        transactions = list(reader)
        return transactions


def reads_financial_transactions_excel(file_path):
    """считывает файл excel, выводит в виде списка словарей"""
    excel_data = pd.read_excel(file_path, parse_dates=["date"])
    transactions = excel_data.to_dict(orient="records")
    return transactions



if __name__ == "__main__":
    result_1 = reads_financial_transactions("C:/Users/Thunderobot/Downloads/transactions.csv")
    result_2 = reads_financial_transactions_excel("C:/Users/Thunderobot/Downloads/transactions_excel.xlsx")
    print(result_1, result_2)