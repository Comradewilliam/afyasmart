import os
import sys

# Add server directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db, Hospital, get_db

# Healthcare facilities data for Tanzania
HOSPITALS = [
    # Dar es Salaam Region
    {
        "name": "Muhimbili National Hospital",
        "type": "Hospital",
        "district": "Ilala",
        "region": "Dar es Salaam",
        "zone": "Eastern",
        "address": "Upanga West, Dar es Salaam",
        "phone": "+255 22 2151593",
        "website": "mnh.or.tz",
        "status": "open",
        "services": "Emergency,Surgery,Pediatrics,Oncology,Cardiology"
    },
    {
        "name": "Aga Khan Hospital",
        "type": "Hospital",
        "district": "Kinondoni",
        "region": "Dar es Salaam",
        "zone": "Eastern",
        "address": "Ocean Road, Dar es Salaam",
        "phone": "+255 22 2115151",
        "website": "agakhanhospitals.org",
        "status": "open",
        "services": "Emergency,Surgery,Pediatrics,Specialist Care"
    },
    {
        "name": "Amana Regional Referral Hospital",
        "type": "Hospital",
        "district": "Ilala",
        "region": "Dar es Salaam",
        "zone": "Eastern",
        "address": "Ilala, Dar es Salaam",
        "phone": "+255 22 2861903",
        "status": "open",
        "services": "Emergency,Surgery,Maternity"
    },
    {
        "name": "Mwananyamala Hospital",
        "type": "Hospital",
        "district": "Kinondoni",
        "region": "Dar es Salaam",
        "zone": "Eastern",
        "address": "Kinondoni, Dar es Salaam",
        "phone": "+255 22 2760500",
        "status": "open",
        "services": "Emergency,Surgery,Pediatrics"
    },
    {
        "name": "Temeke Regional Referral Hospital",
        "type": "Hospital",
        "district": "Temeke",
        "region": "Dar es Salaam",
        "zone": "Eastern",
        "address": "Temeke, Dar es Salaam",
        "phone": "+255 22 2850575",
        "status": "closed",
        "services": "Emergency,Surgery,Pediatrics,Maternity"
    },
    # Kilimanjaro Region
    {
        "name": "Kilimanjaro Christian Medical Centre (KCMC)",
        "type": "Hospital",
        "district": "Moshi",
        "region": "Kilimanjaro",
        "zone": "Northern",
        "address": "Moshi, Kilimanjaro",
        "phone": "+255 27 2754377",
        "website": "kcmc.ac.tz",
        "status": "open",
        "services": "Emergency,Surgery,Pediatrics,Research,Training"
    },
    {
        "name": "Moshi District Hospital",
        "type": "Hospital",
        "district": "Moshi",
        "region": "Kilimanjaro",
        "zone": "Northern",
        "address": "Moshi, Kilimanjaro",
        "phone": "+255 27 2757005",
        "status": "open",
        "services": "Emergency,Surgery,Maternity"
    },
    # Dodoma Region
    {
        "name": "Benjamin Mkapa Hospital (BMH)",
        "type": "Hospital",
        "district": "Dodoma City",
        "region": "Dodoma",
        "zone": "Central",
        "address": "Dodoma",
        "phone": "+255 26 2323000",
        "website": "bmh.or.tz",
        "status": "open",
        "services": "Emergency,Surgery,Specialist Care,Research"
    },
    {
        "name": "Dodoma Regional Referral Hospital",
        "type": "Hospital",
        "district": "Dodoma City",
        "region": "Dodoma",
        "zone": "Central",
        "address": "Dodoma",
        "phone": "+255 26 2324849",
        "status": "open",
        "services": "Emergency,Surgery,Maternity,Pediatrics"
    },
    # Mwanza Region
    {
        "name": "Bugando Medical Centre",
        "type": "Hospital",
        "district": "Nyamagana",
        "region": "Mwanza",
        "zone": "Lake",
        "address": "Mwanza",
        "phone": "+255 28 2500013",
        "website": "bugandomedicalcentre.co.tz",
        "status": "open",
        "services": "Emergency,Surgery,Pediatrics,Specialist Care"
    },
    {
        "name": "Sekou Toure Regional Hospital",
        "type": "Hospital",
        "district": "Nyamagana",
        "region": "Mwanza",
        "zone": "Lake",
        "address": "Mwanza",
        "phone": "+255 28 2500013",
        "status": "open",
        "services": "Emergency,Surgery,Maternity"
    },
    # Mbeya Region
    {
        "name": "Mbeya Zonal Referral Hospital",
        "type": "Hospital",
        "district": "Mbeya City",
        "region": "Mbeya",
        "zone": "Southern",
        "address": "Mbeya",
        "phone": "+255 25 2502291",
        "website": "mzrh.go.tz",
        "status": "open",
        "services": "Emergency,Surgery,Specialist Care"
    },
    {
        "name": "Mbeya Regional Hospital",
        "type": "Hospital",
        "district": "Mbeya City",
        "region": "Mbeya",
        "zone": "Southern",
        "address": "Mbeya",
        "phone": "+255 25 2502291",
        "status": "open",
        "services": "Emergency,Surgery,Primary Care"
    }
]


def seed_hospitals():
    """Seed the database with initial hospital data"""
    from database import SessionLocal
    
    db = SessionLocal()
    try:
        # Clear existing hospitals
        db.query(Hospital).delete()

        # Add new hospitals
        for hospital_data in HOSPITALS:
            hospital = Hospital(**hospital_data)
            db.add(hospital)

        # Commit changes
        db.commit()
        print("Successfully seeded hospital data!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()  # Ensure tables exist
    seed_hospitals()
