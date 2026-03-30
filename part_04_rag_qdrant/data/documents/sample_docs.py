"""Part 4 — Sample hospital documents for RAG ingestion."""

MEDICATION_DISPENSING_POLICY = """\
# Hospital Medication Dispensing Policy
## Policy Number: MED-POL-001
## Department: Pharmacy
## Effective Date: January 1, 2026

### 1. Purpose
This policy establishes guidelines for the safe dispensing of medications throughout City General Hospital.

### 2. Scope
Applies to all licensed pharmacists, pharmacy technicians, nurses, and physicians involved in medication dispensing.

### 3. Controlled Substances
3.1 All Schedule II controlled substances require a handwritten or electronic prescription signed by a licensed prescriber.
3.2 Schedule II prescriptions may not be refilled. A new prescription is required for each dispensing.
3.3 Two-person verification is required when dispensing opioid medications in quantities greater than 30 units.
3.4 All controlled substance transactions must be logged in the Pharmacy Information System within 15 minutes of dispensing.

### 4. Verification Process
4.1 Pharmacist must verify patient identity using two identifiers (name + date of birth).
4.2 Medication label must be reviewed against original prescription for: drug name, strength, dosage form, quantity, directions.
4.3 Drug interaction screening must be performed for all new prescriptions and when adding medications to existing regimens.
4.4 Allergy verification is mandatory before dispensing any new medication.

### 5. High-Alert Medications
The following categories require independent double-check before dispensing:
- Anticoagulants (warfarin, heparin, LMWH)
- Insulin preparations (all types)
- Concentrated electrolytes (KCl >20 mEq, NaCl >0.9%)
- Chemotherapy agents
- Neuromuscular blocking agents

### 6. Pediatric Dispensing
All pediatric medications must have weight-based dosing verified by a clinical pharmacist.
Maximum dose must be checked against current pediatric dosing references.

### 7. Documentation
All dispensed medications must be recorded in the electronic health record (EHR) within 30 minutes.

### 8. Non-Compliance
Failure to follow this policy may result in disciplinary action and regulatory reporting.
"""

PATIENT_PRIVACY_POLICY = """\
# Patient Privacy and Data Protection Policy
## Policy Number: PRIV-POL-005
## Department: Compliance
## Last Updated: March 2026

### 1. HIPAA Compliance
City General Hospital is committed to full compliance with HIPAA Privacy Rule (45 CFR Part 164).
All Protected Health Information (PHI) must be handled according to minimum necessary standards.

### 2. Data Access Controls
2.1 Electronic PHI access is restricted to workforce members with job-related need.
2.2 Audit logs capture all access to electronic health records.
2.3 Passwords must be changed every 90 days. Sharing credentials is prohibited.
2.4 Workstations must auto-lock after 5 minutes of inactivity in clinical areas.

### 3. Disclosure Without Patient Authorization
Permitted disclosures include:
- Treatment, payment, and healthcare operations
- Public health reporting
- Law enforcement activities (with appropriate legal process)
- Serious threat to health or safety

### 4. Patient Rights
Patients have the right to:
- Access their medical records within 30 days of request
- Request corrections to their PHI
- Receive an accounting of disclosures
- Request restrictions on use/disclosure
- Receive notice of privacy practices

### 5. Breach Notification
Any breach of unsecured PHI must be reported to the Privacy Officer within 1 hour of discovery.
Affected patients must be notified within 60 days of discovery.
"""

CARDIOLOGY_TRIAGE_GUIDELINES = """\
# Cardiology Department Triage Guidelines
## Policy Number: CARD-TRIAGE-003
## Department: Cardiology / Emergency
## Version: 2.1

### Chest Pain Assessment Protocol

#### Immediate (Level 1 — Code STEMI):
Activate if patient presents with:
- ST-elevation on 12-lead ECG in ≥2 contiguous leads
- New LBBB with chest pain
- Clinical presentation consistent with acute MI
ACTION: Immediate cath lab activation. Door-to-balloon time < 90 minutes.

#### Urgent (Level 2):
- Troponin elevation without ST-elevation (NSTEMI)
- Unstable angina with rest pain
- New-onset severe chest pain with cardiac risk factors
ACTION: Immediate physician evaluation. IV access, cardiac monitoring, aspirin 325mg.

#### Semi-urgent (Level 3):
- Stable chest pain on exertion
- Atypical chest pain in low-risk patients
- Palpitations without hemodynamic instability
ACTION: Evaluation within 30 minutes. 12-lead ECG, troponin.

### Heart Failure Management
- BNP < 100: Heart failure unlikely
- BNP 100-400: Consider other diagnoses
- BNP > 400: Heart failure likely — initiate workup

### Hypertensive Emergency
Blood pressure > 180/120 with end-organ damage requires immediate IV antihypertensives.
Target: Reduce MAP by no more than 25% in first hour.
"""

APPOINTMENT_SCHEDULING_POLICY = """\
# Appointment Scheduling Policy
## Policy Number: OPS-SCHED-002
## Department: Patient Services

### 1. New Patient Appointments
1.1 New patients require 60-minute initial consultation slots.
1.2 Insurance verification must be completed before appointment confirmation.
1.3 New patients must complete registration forms at least 24 hours before appointment.

### 2. Follow-up Appointments
2.1 Standard follow-up slots are 15 or 30 minutes.
2.2 Follow-ups for complex conditions (cancer, cardiac, neurology) are 45 minutes minimum.
2.3 Post-surgical follow-ups must be scheduled within 14 days of discharge.

### 3. Cancellation Policy
3.1 Patients must cancel at least 24 hours in advance to avoid a no-show fee.
3.2 No-show fee: $50 for standard appointments, $100 for specialist consultations.
3.3 Three consecutive no-shows may result in scheduling restrictions.

### 4. Emergency Same-Day Appointments
4.1 Each physician must reserve 2 slots per day for urgent same-day appointments.
4.2 Triage nurses assess urgency before scheduling same-day slots.

### 5. Telemedicine Appointments
5.1 Available for follow-up visits that do not require physical examination.
5.2 Patient must have reliable internet connection and a compatible device.
5.3 Technical issues lasting > 10 minutes may result in rescheduling without fee.
"""

DRUG_INTERACTION_REFERENCE = """\
# Common Drug Interaction Reference
## Source: Hospital Pharmacy Clinical Reference
## Department: Pharmacy

### High-Risk Interactions (Contraindicated)

**Warfarin + NSAIDs (aspirin, ibuprofen, naproxen)**
Risk: Significantly increased bleeding risk
Action: Avoid combination. If necessary, use lowest effective NSAID dose with close INR monitoring.

**SSRIs + MAOIs**
Risk: Serotonin syndrome (potentially fatal)
Action: Absolute contraindication. Allow 14-day washout period between agents.

**Metformin + IV Contrast**
Risk: Lactic acidosis
Action: Hold metformin 48 hours before and after IV contrast administration.

**ACE Inhibitors + Potassium-Sparing Diuretics + Potassium Supplements**
Risk: Severe hyperkalemia
Action: Monitor potassium closely. Avoid triple combination when possible.

### Moderate Interactions (Use with Caution)

**Statins + Azole Antifungals (fluconazole, ketoconazole)**
Risk: Myopathy, rhabdomyolysis from elevated statin levels
Action: Use lowest statin dose. Avoid atorvastatin/simvastatin with fluconazole if possible.

**Digoxin + Amiodarone**
Risk: Increased digoxin toxicity
Action: Reduce digoxin dose by 50% when initiating amiodarone. Monitor levels.

**Clopidogrel + PPIs (omeprazole, esomeprazole)**
Risk: Reduced clopidogrel efficacy
Action: Prefer pantoprazole when GI protection needed with clopidogrel.

### Monitoring Parameters

| Drug Class | Monitoring | Frequency |
|-----------|-----------|-----------|
| Warfarin | INR | Weekly initially, monthly when stable |
| Digoxin | Drug level, electrolytes | Every 6 months |
| Lithium | Drug level, renal function | Every 3 months |
| Methotrexate | CBC, LFTs, renal function | Monthly |
"""

INFECTION_CONTROL_PROCEDURES = """\
# Infection Control Procedures
## Policy Number: IC-PROC-010
## Department: Infection Control / All Clinical

### 1. Hand Hygiene
1.1 Perform hand hygiene:
- Before touching a patient
- Before clean/aseptic procedures
- After touching patient or surroundings
- After body fluid exposure
- After touching surroundings of patient

1.2 Use alcohol-based hand rub (ABHR) for routine decontamination unless hands are visibly soiled.
1.3 Use soap and water when hands are visibly soiled or after exposure to C. difficile.

### 2. Personal Protective Equipment (PPE)

#### Standard Precautions (all patients):
- Gloves when contact with blood/body fluids expected
- Mask and eye protection for splashing risk

#### Contact Precautions (MRSA, VRE, C. difficile):
- Gown and gloves on entry to patient room
- Dedicated equipment — do not share between patients
- Private room or cohorting required

#### Droplet Precautions (influenza, RSV):
- Surgical mask within 3 feet of patient
- Private room preferred

#### Airborne Precautions (TB, measles, varicella):
- N95 respirator (fit-tested)
- Negative pressure isolation room
- Door must remain closed

### 3. Sharps Safety
3.1 Never recap needles.
3.2 Dispose immediately in puncture-resistant sharps container.
3.3 Sharps containers must be replaced when 3/4 full.

### 4. Isolation Procedures
Patient placement decisions made by Infection Control Practitioners.
Duration of isolation reviewed daily at morning huddle.
"""

BILLING_INSURANCE_GUIDE = """\
# Patient Billing and Insurance Guide
## Department: Patient Financial Services

### Insurance Verification
Before any non-emergency service:
1. Verify insurance eligibility electronically through the billing system
2. Confirm coverage for specific procedure/diagnosis codes
3. Check for pre-authorization requirements
4. Inform patient of estimated out-of-pocket costs

### Common Insurance Terms

**Deductible**: Amount patient pays before insurance coverage begins.
Typical range: $500–$5,000 for individual plans.

**Copay**: Fixed amount paid at time of service (e.g., $30 primary care, $60 specialist).

**Coinsurance**: Percentage patient pays after deductible (e.g., 20% of allowed amount).

**Out-of-Pocket Maximum**: Maximum annual amount patient pays; insurance covers 100% after this.

**Prior Authorization**: Insurance company approval required before certain services.
Common requirements: MRI/CT scans, specialist referrals, elective procedures.

### Billing Codes

**CPT Codes (Procedure)**:
- 99213: Office visit, established patient, low complexity (15–29 min)
- 99214: Office visit, established patient, moderate complexity (30–39 min)
- 99215: Office visit, established patient, high complexity (40–54 min)
- 93000: Electrocardiogram
- 71046: Chest X-ray, 2 views

**ICD-10 Diagnosis Codes**:
- I10: Essential (primary) hypertension
- E11.9: Type 2 diabetes without complications
- J18.9: Pneumonia, unspecified
- M54.5: Low back pain

### Payment Plans
Patients with balances > $500 may qualify for interest-free payment plans (6–24 months).
Financial hardship applications available for patients below 200% of federal poverty level.
"""

EMERGENCY_PROCEDURES = """\
# Emergency Response Procedures
## Policy Number: EM-PROC-001
## Department: Emergency / All Staff

### Code Blue — Cardiac/Respiratory Arrest

1. Call "Code Blue" overhead and activate emergency response (dial ext. 7777)
2. Begin CPR immediately (30:2 ratio for adults)
3. Attach AED/defibrillator as soon as available
4. Assign roles: compressor, airway, IV access, recorder, team leader
5. Administer epinephrine 1mg IV every 3–5 minutes
6. Continue Advanced Cardiac Life Support (ACLS) protocol

### Code Stroke
Activation criteria: Sudden onset of any:
- Facial droop, arm weakness, speech difficulty (FAST assessment)
- Sudden severe headache
- Vision changes
- Sudden confusion or trouble understanding

Time targets:
- CT scan: within 25 minutes of arrival
- CT interpretation: within 45 minutes
- tPA administration (if eligible): within 60 minutes (door-to-needle)

### MET (Medical Emergency Team) Activation
Call MET for any:
- Acute change in conscious state
- Respiratory rate < 8 or > 28 breaths/minute
- SpO2 < 90% despite O2 therapy
- Heart rate < 40 or > 130 bpm
- Systolic BP < 90 mmHg
- Urine output < 50mL over 4 hours

### Mass Casualty Incident (MCI)
Hospital Incident Command System (HICS) activated by Administrator on Call.
Disaster Triage (START method): Immediate (Red), Delayed (Yellow), Minor (Green), Expectant (Black).
"""

CLINICAL_NUTRITION_GUIDELINES = """\
# Clinical Nutrition Guidelines
## Department: Nutrition Services / Clinical Dietetics

### Nutritional Screening
All admitted patients must receive nutritional screening within 24 hours using the Malnutrition Screening Tool (MST).
MST score ≥ 2: Refer to Registered Dietitian within 24 hours.

### Therapeutic Diets

**Cardiac Diet (Heart-Healthy)**:
- Sodium: < 2,000 mg/day
- Saturated fat: < 7% of daily calories
- Trans fat: Eliminate
- Cholesterol: < 200 mg/day
- Increase: Fruits, vegetables, whole grains, omega-3 fatty acids

**Diabetic/Carbohydrate-Controlled Diet**:
- Consistent carbohydrate distribution: 45–60g per meal
- Focus on low glycemic index foods
- Monitor for hypoglycemia in patients on insulin

**Renal Diet**:
- Potassium: 2,000–3,000 mg/day (stage varies)
- Phosphorus: 800–1,000 mg/day
- Protein: 0.6–0.8 g/kg body weight (non-dialysis)
- Fluid restriction per nephrologist order

### Enteral Nutrition
Standard formula: 1.0–1.5 kcal/mL
Start rate: 20–30 mL/hour, advance by 10–20 mL every 4–8 hours

### Parenteral Nutrition
Indicated when GI tract non-functional for > 7 days.
Requires pharmacist, physician, and dietitian collaborative order.
Monitor glucose hourly for first 24 hours.
"""

MENTAL_HEALTH_CRISIS_PROTOCOL = """\
# Mental Health Crisis Assessment Protocol
## Department: Behavioral Health / Emergency

### Risk Assessment (Columbia Suicide Severity Rating Scale)

**Low Risk**:
- Passive suicidal ideation without plan or intent
- No recent attempt
- Action: Safety planning, outpatient referral, crisis line provided

**Moderate Risk**:
- Active ideation with plan but no intent
- Recent (past 30 days) attempt
- Action: Psychiatric consultation within 4 hours, consider voluntary admission

**High Risk (Psychiatric Emergency)**:
- Active ideation with plan AND intent
- Imminent danger to self or others
- Recent attempt in past 24 hours
- Action: Immediate psychiatric evaluation, 1:1 observation, consider 5150/involuntary hold

### De-escalation Techniques
1. Approach calmly and non-threateningly
2. Use the patient's name, speak slowly and clearly
3. Acknowledge feelings without judgment
4. Offer choices to restore sense of control
5. Remove potential hazards from environment
6. Never leave patient alone if actively suicidal

### Documentation Requirements
Every psychiatric assessment must document:
- Risk level classification
- Protective factors
- Safety plan if patient discharged
- Plan to address acute crisis
"""


ALL_DOCUMENTS = {
    "medication_dispensing_policy.txt": (MEDICATION_DISPENSING_POLICY, "Pharmacy", "policy"),
    "patient_privacy_policy.txt": (PATIENT_PRIVACY_POLICY, "Compliance", "policy"),
    "cardiology_triage_guidelines.txt": (CARDIOLOGY_TRIAGE_GUIDELINES, "Cardiology", "clinical_guideline"),
    "appointment_scheduling_policy.txt": (APPOINTMENT_SCHEDULING_POLICY, "Patient Services", "policy"),
    "drug_interaction_reference.txt": (DRUG_INTERACTION_REFERENCE, "Pharmacy", "reference"),
    "infection_control_procedures.txt": (INFECTION_CONTROL_PROCEDURES, "Infection Control", "procedure"),
    "billing_insurance_guide.txt": (BILLING_INSURANCE_GUIDE, "Billing", "guide"),
    "emergency_procedures.txt": (EMERGENCY_PROCEDURES, "Emergency", "procedure"),
    "clinical_nutrition_guidelines.txt": (CLINICAL_NUTRITION_GUIDELINES, "Nutrition", "clinical_guideline"),
    "mental_health_crisis_protocol.txt": (MENTAL_HEALTH_CRISIS_PROTOCOL, "Behavioral Health", "protocol"),
}
