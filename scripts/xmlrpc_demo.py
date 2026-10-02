import xmlrpc.client
import os
import xmlrpc.client

"""
Bien taper les varibles d'environnement dans le terminal avant de lancer le script:
export ODOO_DB=test
export ODOO_USER=admin
export ODOO_PASSWORD=ton_mot_de_passe
"""

url = os.environ.get("ODOO_URL", "http://localhost:8069")
db = os.environ["ODOO_DB"]
user = os.environ["ODOO_USER"]
pwd = os.environ["ODOO_PASSWORD"]

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, user, pwd, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

orders = models.execute_kw(db, uid, pwd, 'sale.order', 'search_read',
    [[['state', '=', 'sale']]],
    {'fields': ['name', 'partner_id', 'amount_total', 'nb_articles'], 'limit': 5})
for o in orders:
    print(o)