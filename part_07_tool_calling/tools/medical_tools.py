"""Part 7 — Medical information and clinical lookup tools."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class DrugInteractionInput(BaseModel):
    drug_a: str = Field(description="First drug name (generic or brand)")
    drug_b: str = Field(description="Second drug name (generic or brand)")


class ICD10LookupInput(BaseModel):
    code: str = Field(description="ICD-10 code to look up (e.g., 'I21.0')")


class DrugInfoInput(BaseModel):
    drug_name: str = Field(description="Drug name (generic or brand)")


_DRUG_INTERACTIONS: dict[tuple[str, str], dict] = {
    ("warfarin", "aspirin"): {
        "severity": "major",
        "description": "Increases bleeding risk significantly.",
        "recommendation": "Avoid combination unless under close medical supervision.",
    },
    ("metformin", "contrast_dye"): {
        "severity": "major",
        "description": "Risk of lactic acidosis with iodinated contrast.",
        "recommendation": "Hold metformin 48h before and after contrast procedures.",
    },
    ("lisinopril", "potassium"): {
        "severity": "moderate",
        "description": "May cause hyperkalemia (high potassium levels).",
        "recommendation": "Monitor potassium levels regularly.",
    },
    ("ssri", "tramadol"): {
        "severity": "major",
        "description": "Risk of serotonin syndrome.",
        "recommendation": "Use with extreme caution; consider alternative analgesia.",
    },
}

_ICD10_CODES: dict[str, dict] = {
    "I21.0": {"description": "Acute transmural myocardial infarction of anterior wall", "category": "Ischemic heart diseases", "billable": True},
    "J18.9": {"description": "Pneumonia, unspecified organism", "category": "Influenza and pneumonia", "billable": True},
    "E11.9": {"description": "Type 2 diabetes mellitus without complications", "category": "Diabetes mellitus", "billable": True},
    "M54.5": {"description": "Low back pain", "category": "Dorsopathies", "billable": True},
    "F32.9": {"description": "Major depressive disorder, single episode, unspecified", "category": "Mood disorders", "billable": True},
    "K21.0": {"description": "Gastro-esophageal reflux disease with esophagitis", "category": "Diseases of esophagus", "billable": True},
    "G43.909": {"description": "Migraine, unspecified, not intractable, without status migrainosus", "category": "Episodic and paroxysmal disorders", "billable": True},
    "N18.3": {"description": "Chronic kidney disease, stage 3 (moderate)", "category": "Renal failure", "billable": True},
}

_DRUG_INFO: dict[str, dict] = {
    "metformin": {
        "generic_name": "Metformin HCl",
        "drug_class": "Biguanide",
        "indications": ["Type 2 diabetes mellitus"],
        "common_doses": ["500 mg twice daily", "850 mg twice daily", "1000 mg twice daily"],
        "common_side_effects": ["nausea", "diarrhea", "metallic taste"],
        "contraindications": ["eGFR < 30", "severe hepatic impairment", "lactic acidosis history"],
    },
    "lisinopril": {
        "generic_name": "Lisinopril",
        "drug_class": "ACE Inhibitor",
        "indications": ["Hypertension", "Heart failure", "Post-MI"],
        "common_doses": ["5 mg daily", "10 mg daily", "20 mg daily", "40 mg daily"],
        "common_side_effects": ["dry cough", "dizziness", "hyperkalemia"],
        "contraindications": ["pregnancy", "angioedema history", "bilateral renal artery stenosis"],
    },
    "atorvastatin": {
        "generic_name": "Atorvastatin Calcium",
        "drug_class": "HMG-CoA reductase inhibitor (Statin)",
        "indications": ["Hyperlipidemia", "Cardiovascular risk reduction"],
        "common_doses": ["10 mg daily", "20 mg daily", "40 mg daily", "80 mg daily"],
        "common_side_effects": ["myalgia", "liver enzyme elevation", "GI upset"],
        "contraindications": ["active liver disease", "pregnancy", "rhabdomyolysis history"],
    },
}


@tool("search_drug_interactions", args_schema=DrugInteractionInput)
async def search_drug_interactions(drug_a: str, drug_b: str) -> dict:
    """Check for known interactions between two drugs. Returns severity and recommendations."""
    key_a = (drug_a.lower(), drug_b.lower())
    key_b = (drug_b.lower(), drug_a.lower())

    interaction = _DRUG_INTERACTIONS.get(key_a) or _DRUG_INTERACTIONS.get(key_b)
    if interaction:
        return {
            "drug_a": drug_a,
            "drug_b": drug_b,
            "interaction_found": True,
            **interaction,
        }
    return {
        "drug_a": drug_a,
        "drug_b": drug_b,
        "interaction_found": False,
        "severity": "none",
        "description": "No known significant interaction found in database.",
        "recommendation": "Always verify with a clinical pharmacist for complete information.",
    }


@tool("lookup_icd10_code", args_schema=ICD10LookupInput)
async def lookup_icd10_code(code: str) -> dict:
    """Look up a diagnosis by its ICD-10 code to get description and billing information."""
    entry = _ICD10_CODES.get(code.upper())
    if not entry:
        return {"error": f"ICD-10 code '{code}' not found in database."}
    return {"code": code.upper(), **entry}


@tool("get_drug_information", args_schema=DrugInfoInput)
async def get_drug_information(drug_name: str) -> dict:
    """Retrieve drug class, indications, dosing, side effects, and contraindications."""
    entry = _DRUG_INFO.get(drug_name.lower())
    if not entry:
        return {
            "error": f"Drug '{drug_name}' not found. Available: {', '.join(_DRUG_INFO.keys())}"
        }
    return {"drug_name": drug_name, **entry}
