from typing import Any, Dict, List, Optional
from fastapi import HTTPException, status

class PharmacyERPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = "PHARMACY_ERP_ERROR",
        invalid_params: Optional[List[Dict[str, Any]]] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.invalid_params = invalid_params or []

class TenantIsolationException(PharmacyERPException):
    def __init__(self, detail: str = "Cross-tenant access violation"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="TENANT_ISOLATION_VIOLATION"
        )

class InsufficientStockException(PharmacyERPException):
    def __init__(self, detail: str, invalid_params: Optional[List[Dict[str, Any]]] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="INSUFFICIENT_STOCK",
            invalid_params=invalid_params
        )

class BatchExpiredException(PharmacyERPException):
    def __init__(self, detail: str = "Attempted allocation of expired or quarantined batch"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="BATCH_EXPIRED_OR_QUARANTINED"
        )

class UnbalancedJournalException(PharmacyERPException):
    def __init__(self, detail: str = "Journal entry does not balance (Debit != Credit)"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="UNBALANCED_JOURNAL_ENTRY"
        )

class AccountingPeriodClosedException(PharmacyERPException):
    def __init__(self, detail: str = "Accounting period is closed against backdated postings"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="ACCOUNTING_PERIOD_CLOSED"
        )

class PrescriptionValidationException(PharmacyERPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="PRESCRIPTION_VALIDATION_ERROR"
        )
