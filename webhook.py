import starkbank
import schedule
from time import sleep
from datetime import date, datetime, timedelta

def pag():
    private_key_content = """
Coloque sua private key
    """

    project = starkbank.Project(
    environment="sandbox",
    id="5515337999056896",
    private_key=private_key_content,)

    organization = starkbank.Organization(
    environment="sandbox",
    id="5631986051842048",
    private_key=private_key_content,
    workspace_id=None,)

    balance = starkbank.balance.get(user=project)

    starkbank.user = project  # or organization

    balance = starkbank.balance.get()

    starkbank.language = "pt-BR"

    invoices = starkbank.invoice.create([
        starkbank.Invoice(
            amount=23571,  # R$ 235,71 
            name="Challenge",
            tax_id="012.345.678-90", 
            due=datetime.utcnow() + timedelta(hours=1),
            expiration=timedelta(hours=3).total_seconds(),
            fine=5,  # 5%
            interest=2.5,  # 2.5% per month
            tags=["immediate"]
        ),
        starkbank.Invoice(
            amount=23571,  # R$ 235,71 
            name="Challenge",
            tax_id="012.345.678-90", 
            due=date(2022, 3, 20),
            expiration=timedelta(hours=3).total_seconds(),
            fine=5,  # 5%
            interest=2.5,  # 2.5% per month
            tags=["scheduled"]
        ),
        starkbank.Invoice(
            amount=23571,  # R$ 235,71 
            name="Challenge",
            tax_id="012.345.678-90", 
            due=datetime.utcnow() + timedelta(hours=1),
            expiration=timedelta(hours=3).total_seconds(),
            fine=5,  # 5%
            interest=2.5,  # 2.5% per month
            tags=["immediate"]
        ),starkbank.Invoice(
            amount=23571,  # R$ 235,71 
            name="Challenge",
            tax_id="012.345.678-90", 
            due=datetime.utcnow() + timedelta(hours=1),
            expiration=timedelta(hours=3).total_seconds(),
            fine=5,  # 5%
            interest=2.5,  # 2.5% per month
            tags=["immediate"]
        ),starkbank.Invoice(
            amount=23571,  # R$ 235,71 
            name="Challenge",
            tax_id="012.345.678-90", 
            due=datetime.utcnow() + timedelta(hours=1),
            expiration=timedelta(hours=3).total_seconds(),
            fine=5,  # 5%
            interest=2.5,  # 2.5% per month
            tags=["immediate"]
        ),starkbank.Invoice(
            amount=23571,  # R$ 235,71 
            name="Challenge",
            tax_id="012.345.678-90", 
            due=datetime.utcnow() + timedelta(hours=1),
            expiration=timedelta(hours=3).total_seconds(),
            fine=5,  # 5%
            interest=2.5,  # 2.5% per month
            tags=["immediate"]
        ),starkbank.Invoice(
            amount=23571,  # R$ 235,71 
            name="Challenge",
            tax_id="012.345.678-90", 
            due=datetime.utcnow() + timedelta(hours=1),
            expiration=timedelta(hours=3).total_seconds(),
            fine=5,  # 5%
            interest=2.5,  # 2.5% per month
            tags=["immediate"]
        ),starkbank.Invoice(
            amount=23571,  # R$ 235,71 
            name="Challenge",
            tax_id="012.345.678-90", 
            due=datetime.utcnow() + timedelta(hours=1),
            expiration=timedelta(hours=3).total_seconds(),
            fine=5,  # 5%
            interest=2.5,  # 2.5% per month
            tags=["immediate"]
        ),
    ])

    for invoice in invoices:
        p = print(invoice)
    
    transfer = starkbank.transfer.create([
    starkbank.Transfer(
    amount=700000,
    bank_code="20018183",  # TED
    branch_code="0001",
    account_number="6341320293482496",
    tax_id="20.018.183/0001-80",
    name="Stark Bank S.A.",
    tags=["payment"]
    )])

    webhooks = starkbank.webhook.query()
    for webhook in webhooks:
        prt = print(webhook)
    return print(transfer), p, prt

schedule.every(3).hours.do(pag)
while 1:
    schedule.run_pending()
    sleep(1)