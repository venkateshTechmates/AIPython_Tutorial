"""Part 7 — Tests for all tool-calling tools."""

import pytest
from unittest.mock import patch
from datetime import date


# ---------------------------------------------------------------------------
# Patient tools
# ---------------------------------------------------------------------------

class TestPatientTools:
    @pytest.mark.asyncio
    async def test_get_patient_by_id_found(self):
        from tools.patient_tools import get_patient_by_id
        result = await get_patient_by_id.ainvoke({"patient_id": 1})
        assert result["patient_id"] == 1
        assert "first_name" in result
        assert "last_name" in result

    @pytest.mark.asyncio
    async def test_get_patient_by_id_not_found(self):
        from tools.patient_tools import get_patient_by_id
        result = await get_patient_by_id.ainvoke({"patient_id": 9999})
        assert "error" in result

    @pytest.mark.asyncio
    async def test_search_patients_by_name(self):
        from tools.patient_tools import search_patients_by_name
        result = await search_patients_by_name.ainvoke({"name": "smith"})
        # Result should be a list or dict with results key
        assert isinstance(result, (list, dict))

    @pytest.mark.asyncio
    async def test_search_patients_no_results(self):
        from tools.patient_tools import search_patients_by_name
        result = await search_patients_by_name.ainvoke({"name": "zzznomatchzzz"})
        assert isinstance(result, (list, dict))


# ---------------------------------------------------------------------------
# Appointment tools
# ---------------------------------------------------------------------------

class TestAppointmentTools:
    @pytest.mark.asyncio
    async def test_schedule_appointment_valid_specialty(self):
        from tools.appointment_tools import schedule_appointment
        result = await schedule_appointment.ainvoke({
            "patient_id": 1,
            "doctor_specialty": "cardiology",
            "preferred_date": "2025-09-15",
            "reason": "Chest pain evaluation",
        })
        assert "appointment_number" in result
        assert result["specialty"] == "cardiology"
        assert "consultation_fee" in result

    @pytest.mark.asyncio
    async def test_schedule_appointment_unknown_specialty(self):
        from tools.appointment_tools import schedule_appointment
        result = await schedule_appointment.ainvoke({
            "patient_id": 1,
            "doctor_specialty": "astrology",
            "preferred_date": "2025-09-15",
            "reason": "Test",
        })
        assert "error" in result

    @pytest.mark.asyncio
    async def test_check_doctor_availability(self):
        from tools.appointment_tools import check_doctor_availability
        result = await check_doctor_availability.ainvoke({"doctor_id": 1, "date": "2025-09-15"})
        assert "available_slots" in result
        assert isinstance(result["available_slots"], list)
        assert len(result["available_slots"]) > 0


# ---------------------------------------------------------------------------
# Billing tools
# ---------------------------------------------------------------------------

class TestBillingTools:
    @pytest.mark.asyncio
    async def test_get_invoice_found(self):
        from tools.billing_tools import get_invoice_by_id
        result = await get_invoice_by_id.ainvoke({"invoice_id": "INV-00001"})
        assert result["invoice_id"] == "INV-00001"
        assert "total" in result
        assert "items" in result

    @pytest.mark.asyncio
    async def test_get_invoice_not_found(self):
        from tools.billing_tools import get_invoice_by_id
        result = await get_invoice_by_id.ainvoke({"invoice_id": "INV-99999"})
        assert "error" in result

    @pytest.mark.asyncio
    async def test_calculate_bill_without_medications(self):
        from tools.billing_tools import calculate_bill
        result = await calculate_bill.ainvoke({
            "appointment_id": "APT-123",
            "include_medications": False,
        })
        assert "subtotal" in result
        assert result["includes_medications"] is False
        assert result["insurance_coverage"] < result["subtotal"]

    @pytest.mark.asyncio
    async def test_calculate_bill_with_medications(self):
        from tools.billing_tools import calculate_bill
        without = await calculate_bill.ainvoke({"appointment_id": "APT-1", "include_medications": False})
        with_meds = await calculate_bill.ainvoke({"appointment_id": "APT-1", "include_medications": True})
        assert with_meds["subtotal"] > without["subtotal"]

    @pytest.mark.asyncio
    async def test_apply_discount(self):
        from tools.billing_tools import apply_discount
        result = await apply_discount.ainvoke({
            "invoice_id": "INV-00001",
            "discount_percent": 20.0,
            "reason": "insurance_adjustment",
        })
        assert result["discount_percent"] == 20.0
        assert result["new_total"] < result["original_total"]

    @pytest.mark.asyncio
    async def test_apply_discount_invoice_not_found(self):
        from tools.billing_tools import apply_discount
        result = await apply_discount.ainvoke({
            "invoice_id": "INV-FAKE",
            "discount_percent": 10.0,
            "reason": "test",
        })
        assert "error" in result


# ---------------------------------------------------------------------------
# Medical tools
# ---------------------------------------------------------------------------

class TestMedicalTools:
    @pytest.mark.asyncio
    async def test_search_drug_interactions_found(self):
        from tools.medical_tools import search_drug_interactions
        result = await search_drug_interactions.ainvoke({"drug_a": "warfarin", "drug_b": "aspirin"})
        assert result["interaction_found"] is True
        assert result["severity"] == "major"

    @pytest.mark.asyncio
    async def test_search_drug_interactions_reversed_order(self):
        from tools.medical_tools import search_drug_interactions
        result = await search_drug_interactions.ainvoke({"drug_a": "aspirin", "drug_b": "warfarin"})
        assert result["interaction_found"] is True

    @pytest.mark.asyncio
    async def test_search_drug_interactions_none(self):
        from tools.medical_tools import search_drug_interactions
        result = await search_drug_interactions.ainvoke({"drug_a": "vitamin_c", "drug_b": "water"})
        assert result["interaction_found"] is False

    @pytest.mark.asyncio
    async def test_lookup_icd10_code_found(self):
        from tools.medical_tools import lookup_icd10_code
        result = await lookup_icd10_code.ainvoke({"code": "I21.0"})
        assert "description" in result
        assert result["code"] == "I21.0"
        assert result["billable"] is True

    @pytest.mark.asyncio
    async def test_lookup_icd10_code_not_found(self):
        from tools.medical_tools import lookup_icd10_code
        result = await lookup_icd10_code.ainvoke({"code": "ZZZ99.9"})
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_drug_information_found(self):
        from tools.medical_tools import get_drug_information
        result = await get_drug_information.ainvoke({"drug_name": "metformin"})
        assert result["drug_name"] == "metformin"
        assert "drug_class" in result
        assert "contraindications" in result

    @pytest.mark.asyncio
    async def test_get_drug_information_not_found(self):
        from tools.medical_tools import get_drug_information
        result = await get_drug_information.ainvoke({"drug_name": "dragonroot"})
        assert "error" in result


# ---------------------------------------------------------------------------
# Utility tools
# ---------------------------------------------------------------------------

class TestUtilityTools:
    @pytest.mark.asyncio
    async def test_get_current_datetime(self):
        from tools.utility_tools import get_current_datetime
        result = await get_current_datetime.ainvoke({})
        assert "date" in result
        assert "time" in result
        assert "day_of_week" in result

    @pytest.mark.asyncio
    async def test_calculate_patient_age_valid(self):
        from tools.utility_tools import calculate_patient_age
        result = await calculate_patient_age.ainvoke({"date_of_birth": "1990-06-15"})
        assert "age_years" in result
        assert result["age_years"] >= 34
        assert "age_category" in result

    @pytest.mark.asyncio
    async def test_calculate_patient_age_future_dob(self):
        from tools.utility_tools import calculate_patient_age
        result = await calculate_patient_age.ainvoke({"date_of_birth": "2099-01-01"})
        assert "error" in result

    @pytest.mark.asyncio
    async def test_calculate_patient_age_invalid_format(self):
        from tools.utility_tools import calculate_patient_age
        result = await calculate_patient_age.ainvoke({"date_of_birth": "not-a-date"})
        assert "error" in result

    @pytest.mark.asyncio
    async def test_format_medical_date_valid(self):
        from tools.utility_tools import format_medical_date
        result = await format_medical_date.ainvoke({"date_str": "2025-01-15"})
        assert result["iso"] == "2025-01-15"
        assert "formatted" in result

    @pytest.mark.asyncio
    async def test_format_medical_date_invalid(self):
        from tools.utility_tools import format_medical_date
        result = await format_medical_date.ainvoke({"date_str": "not a date at all"})
        assert "error" in result
