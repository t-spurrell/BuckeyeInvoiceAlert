from requests import get


class InvoiceNinja:

    def __init__(self, host, token):
        self.host = host
        self.token = token

    def get_client_name(self, client_id):
        url = f'{self.host}/clients/{client_id}'
        headers = {'X-API-Token': self.token, 'Content-Type': 'application/json'}
        response = get(url=url, headers=headers)
        if response.ok:
            data = response.json()
            client_name = data['data']['name']
            return client_name

    def get_overdue_invoices(self):
        url = f'{self.host}/invoices?status=active&filter_deleted_clients=true&overdue=true'
        headers = {'X-API-Token': self.token, 'Content-Type': 'application/json'}
        response = get(url=url, headers=headers)
        if response.ok:
            data = response.json()
            overdue = data['data']
            return overdue
