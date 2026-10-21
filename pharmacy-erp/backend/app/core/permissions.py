from enum import Enum

class PermissionCode(str, Enum):
    # Medicine Catalog
    MEDICINE_READ = "medicine.read"
    MEDICINE_CREATE = "medicine.create"
    MEDICINE_UPDATE = "medicine.update"
    
    # Inventory
    INVENTORY_READ = "inventory.read"
    INVENTORY_LEDGER_READ = "inventory.ledger.read"
    INVENTORY_ADJUST = "inventory.adjust"
    INVENTORY_ADJUST_APPROVE = "inventory.adjust.approve"
    INVENTORY_QUARANTINE = "inventory.quarantine"
    INVENTORY_TRANSFER_CREATE = "inventory.transfer.create"
    INVENTORY_TRANSFER_RECEIVE = "inventory.transfer.receive"
    
    # Procurement
    PURCHASE_READ = "purchase.read"
    PURCHASE_CREATE = "purchase.create"
    PURCHASE_APPROVE = "purchase.approve"
    GRN_CREATE = "grn.create"
    GRN_POST = "grn.post"
    PURCHASE_RETURN = "purchase.return"
    
    # Sales POS & Wholesale
    POS_SALE_CREATE = "pos.sale.create"
    POS_SESSION_MANAGE = "pos.session.manage"
    SALE_INVOICE_READ = "sale.invoice.read"
    SALE_RETURN = "sale.return"
    WHOLESALE_ORDER_CREATE = "wholesale.order.create"
    WHOLESALE_ORDER_DISPATCH = "wholesale.order.dispatch"
    
    # Prescriptions & Dispensing
    PRESCRIPTION_READ = "prescription.read"
    PRESCRIPTION_CREATE = "prescription.create"
    PRESCRIPTION_REVIEW = "prescription.review"
    DISPENSING_APPROVE = "dispensing.approve"
    REGISTER_H1_READ = "register.h1.read"
    
    # Accounting
    ACCOUNTING_CHART_READ = "accounting.chart.read"
    ACCOUNTING_CHART_MANAGE = "accounting.chart.manage"
    ACCOUNTING_JOURNAL_READ = "accounting.journal.read"
    ACCOUNTING_JOURNAL_CREATE = "accounting.journal.create"
    ACCOUNTING_JOURNAL_REVERSE = "accounting.journal.reverse"
    ACCOUNTING_PERIOD_READ = "accounting.period.read"
    ACCOUNTING_PERIOD_CLOSE = "accounting.period.close"
    ACCOUNTING_REPORT_READ = "accounting.report.read"
    
    # Organization & Admin
    ORGANIZATION_READ = "organization.read"
    ORGANIZATION_UPDATE = "organization.update"
    BRANCH_READ = "branch.read"
    BRANCH_CREATE = "branch.create"
    USER_READ = "user.read"
    USER_CREATE = "user.create"
    ROLE_READ = "role.read"
