import notes
import os
import pandas as pd
from teams import TeamsConfig
from configuration import load_config, file_exist
from invoice_ninja import InvoiceNinja

CONFIG = load_config()

#Auth to InvoiceNinja api
invoice_ninja_conn = InvoiceNinja(host=CONFIG['invoice_ninja']['base_url'], token=CONFIG['invoice_ninja']['token'])


def send_to_teams(body) -> None:
    message = TeamsConfig(CONFIG['url'])
    message.color("ff4000")
    message.text(body)
    message.send()


def previously_notified(invoice_id) -> bool:
    if file_exist('notified'):
        with open('notified', 'r') as f:
            data = f.read()
            if str(invoice_id) in data:
                return True
            else:
                return False


def first_of_month() -> None:
    day = pd.Timestamp.today()
    if day.is_month_start:
        if file_exist('notified'):
            os.remove('notified')


def main():
    first_of_month()

    overdue = []
    ninja_overdue = invoice_ninja_conn.get_overdue_invoices()

    if ninja_overdue:
        for o in ninja_overdue:
            invoice_id = o['number']
            if not previously_notified(invoice_id):
                client_id = o['client_id']
                client_name = invoice_ninja_conn.get_client_name(client_id)
                balance = o['balance']
                due_date = o['due_date']
                days_late = pd.Timestamp.today() - pd.Timestamp(due_date)
                with open('notified', 'a') as f:
                    f.write(str(invoice_id) + '\n')
                client = {
                    'name': client_name,
                    'invoice_id': invoice_id,
                    'balance': balance,
                    'days_late': days_late.days
                }
                overdue.append(client)
        if overdue:
            body = notes.overdue(overdue)
            send_to_teams(body)
            #print(body)
        else:
            print('no overdue clients')


if __name__ == '__main__':
    main()






