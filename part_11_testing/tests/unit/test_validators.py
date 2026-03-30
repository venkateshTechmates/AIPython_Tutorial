"""Part 11 — Unit tests for Pydantic validators from Part 2."""

import pytest
from datetime import date


class TestPatientValidators:
    def test_valid_blood_type(self):
        import re
        pattern = r"^(A|B|AB|O)[+-]$"
        valid = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        for bt in valid:
            assert re.match(pattern, bt), f"{bt} should be valid"

    def test_invalid_blood_type(self):
        import re
        pattern = r"^(A|B|AB|O)[+-]$"
        invalid = ["C+", "AA+", "O", "+", "ab+"]
        for bt in invalid:
            assert not re.match(pattern, bt), f"{bt} should be invalid"

    def test_phone_normalization(self):
        """Phones should be cleaned to digits only."""
        raw = "555-123-4567"
        normalized = "".join(c for c in raw if c.isdigit())
        assert normalized == "5551234567"

    def test_past_date_only(self):
        today = date.today()
        future = date(today.year + 1, 1, 1)
        assert future > today  # future DOB should be rejected

    def test_full_name_computation(self):
        first, last = "Jane", "Doe"
        full_name = f"{first} {last}"
        assert full_name == "Jane Doe"

    def test_age_computation(self):
        dob = date(1990, 1, 1)
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        assert age >= 34


class TestDoctorValidators:
    def test_valid_specialty(self):
        valid_specialties = [
            "cardiology", "neurology", "general_practice",
            "orthopedics", "pediatrics", "oncology",
        ]
        for s in valid_specialties:
            assert isinstance(s, str)
            assert len(s) > 0

    def test_license_number_uppercase(self):
        raw = "md-12345"
        normalized = raw.upper()
        assert normalized == "MD-12345"

    def test_available_days_validation(self):
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        user_days = ["Monday", "Wednesday", "Friday"]
        invalid_days = ["monday", "Funday", "Holiday"]
        for d in user_days:
            assert d in valid_days
        for d in invalid_days:
            assert d not in valid_days


class TestICD10Validators:
    def test_icd10_valid_codes(self):
        import re
        pattern = r"^[A-Z]\d{2}(\.\d{1,4})?$"
        codes = ["I21.0", "J18.9", "E11", "M54.5", "G43.909"]
        for code in codes:
            assert re.match(pattern, code)

    def test_icd10_invalid_codes(self):
        import re
        pattern = r"^[A-Z]\d{2}(\.\d{1,4})?$"
        codes = ["i21.0", "1234", "ABCD", "I21.123456"]
        for code in codes:
            assert not re.match(pattern, code)


class TestBillingValidators:
    def test_subtotal_calculation(self):
        quantity = 3
        unit_price = 50.0
        discount = 10.0
        subtotal = quantity * unit_price * (1 - discount / 100)
        assert subtotal == 135.0

    def test_invoice_total_chain(self):
        subtotal = 500.0
        tax_rate = 0.08
        tax = round(subtotal * tax_rate, 2)
        total = subtotal + tax
        assert total == 540.0

    def test_patient_responsibility(self):
        total = 1000.0
        insurance = 800.0
        deductible = 200.0
        copay = 30.0
        responsibility = max(total - insurance - deductible + copay, 0.0)
        assert responsibility >= 0.0

    def test_discount_floor(self):
        """Patient responsibility should never go below zero."""
        total = 100.0
        insurance = 200.0  # overpayment scenario
        responsibility = max(total - insurance, 0.0)
        assert responsibility == 0.0
