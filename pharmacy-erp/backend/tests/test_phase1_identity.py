import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

def test_onboard_organization_and_login(client: TestClient):
    # 1. Onboard Organization
    payload = {
        "organization": {
            "legal_name": "Apollo Pharmacy Retail Ltd",
            "trade_name": "Apollo Pharmacy #104",
            "gstin": "27AAACA1234A1Z5",
            "pan": "AAACA1234A",
            "drug_license_retail": "MH-TZ-20-49210",
            "currency": "INR"
        },
        "admin_name": "Dr. Rajesh Sharma",
        "admin_email": "rajesh.sharma@apollopharmacy.in",
        "admin_phone": "+919820012345",
        "admin_password": "SecurePassword#2026",
        "initial_branch": {
            "branch_code": "AP-MUM-01",
            "name": "Bandra West Flagship Store",
            "branch_type": "RETAIL",
            "state_code": "27",
            "gstin": "27AAACA1234A1Z5",
            "drug_license_number": "MH-TZ-20-49210",
            "pharmacist_in_charge_name": "Dr. Rajesh Sharma",
            "pharmacist_reg_number": "MH-PH-8921",
            "address_line1": "Hill Road, Bandra West",
            "city": "Mumbai",
            "pincode": "400050",
            "phone": "+919820012345",
            "email": "bandra@apollopharmacy.in"
        }
    }

    response = client.post("/api/v1/auth/onboard", json=payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "rajesh.sharma@apollopharmacy.in"
    assert data["active_branch_id"] is not None
    assert len(data["permissions"]) > 0

    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Query current organization
    org_res = client.get("/api/v1/organizations/current", headers=headers)
    assert org_res.status_code == 200
    assert org_res.json()["legal_name"] == "Apollo Pharmacy Retail Ltd"

    # 3. List branches
    branch_res = client.get("/api/v1/branches", headers=headers)
    assert branch_res.status_code == 200
    branches = branch_res.json()
    assert len(branches) == 1
    assert branches[0]["branch_code"] == "AP-MUM-01"

    # 4. List roles
    role_res = client.get("/api/v1/roles", headers=headers)
    assert role_res.status_code == 200
    roles = role_res.json()
    assert any(r["name"] == "Pharmacy Owner" for r in roles)


def test_invalid_credentials_rejected(client: TestClient):
    response = client.post("/api/v1/auth/login", json={
        "email": "nonexistent@pharmacy.in",
        "password": "WrongPassword123"
    })
    assert response.status_code == 401
    assert response.json()["title"] == "INVALID_CREDENTIALS"


def test_tenant_isolation_strictly_enforced(client: TestClient):
    # Onboard Tenant A
    res_a = client.post("/api/v1/auth/onboard", json={
        "organization": {
            "legal_name": "Tenant A Healthcare",
            "trade_name": "Tenant A Pharmacy",
            "pan": "AAAAA1111A",
            "currency": "INR"
        },
        "admin_name": "Admin Tenant A",
        "admin_email": "admin@tenant-a.com",
        "admin_phone": "+919800000001",
        "admin_password": "PasswordA#2026",
        "initial_branch": {
            "branch_code": "BR-A1",
            "name": "Branch A1",
            "branch_type": "RETAIL",
            "state_code": "27",
            "drug_license_number": "DL-A1",
            "address_line1": "Street A",
            "city": "Mumbai",
            "pincode": "400001",
            "phone": "+919800000001"
        }
    })
    assert res_a.status_code == 201
    token_a = res_a.json()["access_token"]
    org_id_a = res_a.json()["user"]["organization_id"]

    # Onboard Tenant B
    res_b = client.post("/api/v1/auth/onboard", json={
        "organization": {
            "legal_name": "Tenant B Healthcare",
            "trade_name": "Tenant B Pharmacy",
            "pan": "BBBBB2222B",
            "currency": "INR"
        },
        "admin_name": "Admin Tenant B",
        "admin_email": "admin@tenant-b.com",
        "admin_phone": "+919800000002",
        "admin_password": "PasswordB#2026",
        "initial_branch": {
            "branch_code": "BR-B1",
            "name": "Branch B1",
            "branch_type": "RETAIL",
            "state_code": "27",
            "drug_license_number": "DL-B1",
            "address_line1": "Street B",
            "city": "Pune",
            "pincode": "411001",
            "phone": "+919800000002"
        }
    })
    assert res_b.status_code == 201
    token_b = res_b.json()["access_token"]
    org_id_b = res_b.json()["user"]["organization_id"]

    assert org_id_a != org_id_b

    # Tenant A querying branches must ONLY see Tenant A's branches
    headers_a = {"Authorization": f"Bearer {token_a}"}
    branches_a = client.get("/api/v1/branches", headers=headers_a).json()
    assert len(branches_a) == 1
    assert branches_a[0]["branch_code"] == "BR-A1"

    # Tenant B querying branches must ONLY see Tenant B's branches
    headers_b = {"Authorization": f"Bearer {token_b}"}
    branches_b = client.get("/api/v1/branches", headers=headers_b).json()
    assert len(branches_b) == 1
    assert branches_b[0]["branch_code"] == "BR-B1"

    # Tenant A attempting to switch branch to Tenant B's branch must be strictly forbidden
    tenant_b_branch_id = branches_b[0]["id"]
    switch_res = client.post(
        "/api/v1/auth/switch-branch",
        json={"branch_id": tenant_b_branch_id},
        headers=headers_a
    )
    assert switch_res.status_code == 403


def test_branch_creation_and_switching(client: TestClient):
    # Onboard Multi-Branch Organization
    res = client.post("/api/v1/auth/onboard", json={
        "organization": {
            "legal_name": "Multi Branch Meds Pvt Ltd",
            "trade_name": "Multi Branch Meds",
            "pan": "MBMED1234A",
            "currency": "INR"
        },
        "admin_name": "General Manager",
        "admin_email": "gm@multibranch.com",
        "admin_phone": "+919999900000",
        "admin_password": "PasswordGM#2026",
        "initial_branch": {
            "branch_code": "MB-HQ",
            "name": "Headquarters Retail",
            "branch_type": "RETAIL",
            "state_code": "27",
            "drug_license_number": "DL-HQ-01",
            "address_line1": "HQ Road",
            "city": "Mumbai",
            "pincode": "400001",
            "phone": "+919999900000"
        }
    })
    assert res.status_code == 201
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Add second branch (Wholesale Depot)
    branch2_res = client.post("/api/v1/branches", json={
        "branch_code": "MB-DEPOT",
        "name": "Bhiwandi Central Depot",
        "branch_type": "WHOLESALE_DEPOT",
        "state_code": "27",
        "drug_license_number": "DL-DEPOT-02",
        "address_line1": "Logistics Park, Bhiwandi",
        "city": "Thane",
        "pincode": "421302",
        "phone": "+919999900001"
    }, headers=headers)
    assert branch2_res.status_code == 201
    branch2_id = branch2_res.json()["id"]

    # List branches (should now have 2)
    all_branches = client.get("/api/v1/branches", headers=headers).json()
    assert len(all_branches) == 2

    # Duplicate branch code within same org must fail
    dup_res = client.post("/api/v1/branches", json={
        "branch_code": "MB-DEPOT",
        "name": "Another Depot",
        "branch_type": "RETAIL",
        "state_code": "27",
        "drug_license_number": "DL-003",
        "address_line1": "Some St",
        "city": "Thane",
        "pincode": "421302",
        "phone": "+919999900002"
    }, headers=headers)
    assert dup_res.status_code == 409


def test_rbac_permission_enforcement(client: TestClient):
    # 1. Onboard Org
    res = client.post("/api/v1/auth/onboard", json={
        "organization": {
            "legal_name": "RBAC Test Org",
            "trade_name": "RBAC Meds",
            "pan": "RBACT1234A",
            "currency": "INR"
        },
        "admin_name": "Admin Owner",
        "admin_email": "admin@rbactest.com",
        "admin_phone": "+919888800001",
        "admin_password": "AdminPassword#2026",
        "initial_branch": {
            "branch_code": "RBAC-B1",
            "name": "Store 1",
            "branch_type": "RETAIL",
            "state_code": "27",
            "drug_license_number": "DL-RBAC-01",
            "address_line1": "Street 1",
            "city": "Mumbai",
            "pincode": "400001",
            "phone": "+919888800001"
        }
    })
    admin_token = res.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    branch_id = res.json()["active_branch_id"]

    # 2. Create Cashier Role with only POS permissions
    cashier_role_res = client.post("/api/v1/roles", json={
        "name": "POS Cashier",
        "description": "Cashier restricted to retail POS checkout only",
        "permission_ids": []
    }, headers=admin_headers)
    assert cashier_role_res.status_code == 201
    cashier_role_id = cashier_role_res.json()["id"]

    # 3. Create Cashier User assigned to POS Cashier Role
    cashier_user_res = client.post("/api/v1/users", json={
        "email": "cashier1@rbactest.com",
        "phone": "+919888800002",
        "password": "CashierPassword#2026",
        "full_name": "Anil Cashier",
        "role_id": cashier_role_id,
        "branch_id": branch_id
    }, headers=admin_headers)
    assert cashier_user_res.status_code == 201

    # 4. Login as Cashier
    cashier_login_res = client.post("/api/v1/auth/login", json={
        "email": "cashier1@rbactest.com",
        "password": "CashierPassword#2026",
        "branch_id": branch_id
    })
    assert cashier_login_res.status_code == 200
    cashier_token = cashier_login_res.json()["access_token"]
    cashier_headers = {"Authorization": f"Bearer {cashier_token}"}

    # 5. Cashier attempts to update Organization settings (Requires organization.update) -> 403 Forbidden
    forbidden_res = client.put(
        "/api/v1/organizations/current",
        json={"trade_name": "Hacked Name"},
        headers=cashier_headers
    )
    assert forbidden_res.status_code == 403
    assert "Permission denied" in forbidden_res.json()["detail"]
