import smtplib
import notes
from email.message import EmailMessage
from configuration import load_config, file_exist
from invoice_ninja import InvoiceNinja

CONFIG = load_config()

#Auth to InvoiceNinja api
invoice_ninja_conn = InvoiceNinja(host=CONFIG['invoice_ninja']['base_url'], token=CONFIG['invoice_ninja']['token'])


def sendEmail(body=None):
    pw = CONFIG['email']['pw']
    msg = EmailMessage()
    msg['Subject'] = f'test'
    msg['From'] = CONFIG['email']['address']
    msg['To'] = CONFIG['email']['to']
    msg.set_content(f'test')

    with smtplib.SMTP('smtp.office365.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(CONFIG['email']['address'], pw)
        smtp.send_message(msg)


def previously_notified(invoice_id):
    if file_exist('notified'):
        with open('notified', 'r') as f:
            data = f.read()
            if str(invoice_id) in data:
                return True
            else:
                return False


def main():
    overdue = []
    ninja_overdue = invoice_ninja_conn.get_overdue_invoices()

    if ninja_overdue:
        for o in ninja_overdue:
            invoice_id = o['number']
            if not previously_notified(invoice_id):
                client_id = o['client_id']
                client_name = invoice_ninja_conn.get_client_name(client_id)
                balance = o['balance']
                print(f'Client: {client_name} with invoice number {invoice_id} has a past due amount of ${balance}')
                with open('notified', 'a') as f:
                    f.write(str(invoice_id) + '\n')
                client = {
                    'name': client_name,
                    'invoice_id': invoice_id,
                    'balance': balance
                }
                overdue.append(client)
        if overdue:
            print('send email')
            body = notes.overdue(overdue)
            print(body)
        else:
            print('no overdue clients')


if __name__ == '__main__':
    main()
    #sendEmail()


