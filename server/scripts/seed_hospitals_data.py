import os
import sys

# Add server directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, Hospital

# Zone mapping based on regions
def get_zone(region):
    eastern_zone = ['Dar es Salaam', 'Morogoro', 'Pwani', 'Tanga']
    northern_zone = ['Arusha', 'Kilimanjaro', 'Manyara', 'Tanga']
    central_zone = ['Dodoma', 'Singida']
    western_zone = ['Katavi', 'Kigoma', 'Tabora']
    lake_zone = ['Geita', 'Kagera', 'Mara', 'Mwanza', 'Shinyanga', 'Simiyu']
    southern_highlands = ['Iringa', 'Mbeya', 'Njombe', 'Rukwa', 'Ruvuma', 'Songwe']
    southern_zone = ['Lindi', 'Mtwara']
    
    if region in eastern_zone:
        return 'Eastern'
    elif region in northern_zone:
        return 'Northern'
    elif region in central_zone:
        return 'Central'
    elif region in western_zone:
        return 'Western'
    elif region in lake_zone:
        return 'Lake'
    elif region in southern_highlands:
        return 'Southern Highlands'
    elif region in southern_zone:
        return 'Southern'
    else:
        return 'Other'

# Hospital types mapping based on names
def get_hospital_type(name):
    if any(x in name.lower() for x in ['national', 'referral', 'zonal']):
        return 'Referral'
    elif 'regional' in name.lower():
        return 'Regional'
    elif 'district' in name.lower():
        return 'District'
    else:
        return 'Private'

hospitals_data = [
    {
        "name": "Muhimbili National Hospital",
        "district": "Ilala",
        "region": "Dar es Salaam",
        "address": "Upanga West, Dar es Salaam",
        "phone": "+255 22 2151593",
        "website": "mnh.or.tz",
        "status": "open",
    },
    {
        "name": "Aga Khan Hospital",
        "district": "Kinondoni",
        "region": "Dar es Salaam",
        "address": "Ocean Road, Dar es Salaam",
        "phone": "+255 22 2115151",
        "website": "agakhanhospitals.org",
        "status": "open",
    },
    {
        "name": "Amana Regional Referral Hospital",
        "district": "Ilala",
        "region": "Dar es Salaam",
        "address": "Ilala, Dar es Salaam",
        "phone": "+255 22 2861903",
        "status": "open",
    },
    {
        "name": "Mwananyamala Hospital",
        "district": "Kinondoni",
        "region": "Dar es Salaam",
        "address": "Kinondoni, Dar es Salaam",
        "phone": "+255 22 2760500",
        "status": "open",
    },
    {
        "name": "Temeke Regional Referral Hospital",
        "district": "Temeke",
        "region": "Dar es Salaam",
        "address": "Temeke, Dar es Salaam",
        "phone": "+255 22 2850575",
        "status": "closed",
    },
    {
        "name": "Kilimanjaro Christian Medical Centre (KCMC)",
        "district": "Moshi",
        "region": "Kilimanjaro",
        "address": "Moshi, Kilimanjaro",
        "phone": "+255 27 2754377",
        "website": "kmc.ac.tz",
        "status": "open",
    },
    {
        "name": "Moshi District Hospital",
        "district": "Moshi",
        "region": "Kilimanjaro",
        "address": "Moshi, Kilimanjaro",
        "phone": "+255 27 2757005",
        "status": "open",
    },
    {
        "name": "Hai District Hospital",
        "district": "Hai",
        "region": "Kilimanjaro",
        "address": "Bomang'ombe, Kilimanjaro",
        "phone": "+255 27 2757005",
        "status": "open",
    },
    {
        "name": "Machame Lutheran Hospital",
        "district": "Hai",
        "region": "Kilimanjaro",
        "address": "Machame, Kilimanjaro",
        "phone": "+255 27 2757005",
        "status": "open",
    },
    {
        "name": "Kibosho Hospital",
        "district": "Moshi",
        "region": "Kilimanjaro",
        "address": "Kibosho, Kilimanjaro",
        "phone": "+255 27 2757005",
        "status": "open",
    },
    {
        "name": "Mount Meru Regional Referral Hospital",
        "district": "Arusha City",
        "region": "Arusha",
        "address": "Arusha",
        "phone": "+255 27 2502329",
        "status": "open",
    },
    {
        "name": "Selian Lutheran Hospital",
        "district": "Arusha City",
        "region": "Arusha",
        "address": "Arusha",
        "phone": "+255 27 2508030",
        "status": "open",
    },
    {
        "name": "Arusha Lutheran Medical Centre (ALMC)",
        "district": "Arusha City",
        "region": "Arusha",
        "address": "Arusha",
        "phone": "+255 27 2508030",
        "status": "open",
    },
    {
        "name": "Benjamin Mkapa Hospital (BMH)",
        "district": "Dodoma City",
        "region": "Dodoma",
        "address": "Dodoma",
        "phone": "+255 26 2323000",
        "website": "bmh.or.tz",
        "status": "open",
    },
    {
        "name": "Dodoma Regional Referral Hospital",
        "district": "Dodoma City",
        "region": "Dodoma",
        "address": "Dodoma",
        "phone": "+255 26 2323000",
        "status": "open",
    },
    {
        "name": "Dodoma Christian Medical Centre (DCMC)",
        "district": "Dodoma City",
        "region": "Dodoma",
        "address": "Dodoma",
        "phone": "+255 26 2323000",
        "status": "open",
    },
    {
        "name": "Mirembe National Mental Health Hospital",
        "district": "Dodoma City",
        "region": "Dodoma",
        "address": "Dodoma",
        "phone": "+255 26 2323000",
        "status": "open",
    },
    {
        "name": "Bugando Medical Centre",
        "district": "Nyamagana",
        "region": "Mwanza",
        "address": "Mwanza",
        "phone": "+255 28 2500013",
        "website": "bugandomedicalcentre.co.tz",
        "status": "open",
    },
    {
        "name": "Kamanga Medics Hospital",
        "district": "Nyamagana",
        "region": "Mwanza",
        "address": "Mwanza",
        "phone": "+255 28 2500013",
        "status": "open",
    },
    {
        "name": "CF Hospital",
        "district": "Nyamagana",
        "region": "Mwanza",
        "address": "Mwanza",
        "phone": "+255 28 2500013",
        "status": "open",
    },
    {
        "name": "Mwananchi Hospital",
        "district": "Nyamagana",
        "region": "Mwanza",
        "address": "Mwanza",
        "phone": "+255 28 2500013",
        "status": "open",
    },
    {
        "name": "Mbeya Zonal Referral Hospital",
        "district": "Mbeya City",
        "region": "Mbeya",
        "address": "Mbeya",
        "phone": "+255 25 2502291",
        "website": "mzrh.go.tz",
        "status": "open",
    },
    {
        "name": "Mbeya Regional Hospital",
        "district": "Mbeya City",
        "region": "Mbeya",
        "address": "Mbeya",
        "phone": "+255 25 2502291",
        "status": "open",
    },
    {
        "name": "Mbarali District Hospital",
        "district": "Mbarali",
        "region": "Mbeya",
        "address": "Rujewa, Mbeya",
        "phone": "+255 25 2502291",
        "status": "open",
    },
    {
        "name": "K's Hospital",
        "district": "Mbeya City",
        "region": "Mbeya",
        "address": "Mbeya",
        "phone": "+255 25 2502291",
        "status": "open",
    },
    {
        "name": "Bombo Regional Referral Hospital",
        "district": "Tanga City",
        "region": "Tanga",
        "address": "Tanga",
        "phone": "+255 27 2643440",
        "status": "open",
    },
    {
        "name": "Ngamiani Hospital",
        "district": "Tanga City",
        "region": "Tanga",
        "address": "Tanga",
        "phone": "+255 27 2643440",
        "status": "open",
    },
    {
        "name": "Makorora Hospital",
        "district": "Tanga City",
        "region": "Tanga",
        "address": "Tanga",
        "phone": "+255 27 2643440",
        "status": "open",
    },
    {
        "name": "Hospital Teule Muheza",
        "district": "Muheza",
        "region": "Tanga",
        "address": "Muheza, Tanga",
        "phone": "+255 27 2644121",
        "status": "open",
    },
    {
        "name": "Morogoro Regional Referral Hospital",
        "district": "Morogoro Municipality",
        "region": "Morogoro",
        "address": "Morogoro",
        "phone": "+255 23 2603485",
        "status": "open",
    },
    {
        "name": "Sokoine University of Agriculture (SUA) Hospital",
        "district": "Morogoro Municipality",
        "region": "Morogoro",
        "address": "Morogoro",
        "phone": "+255 23 2603485",
        "status": "open",
    },
    {
        "name": "Ifakara District Hospital",
        "district": "Kilombero",
        "region": "Morogoro",
        "address": "Ifakara, Morogoro",
        "phone": "+255 23 2603485",
        "status": "open",
    },
    {
        "name": "Mpanda District Hospital",
        "district": "Mpanda",
        "region": "Katavi",
        "address": "Mpanda, Katavi",
        "phone": "+255 26 2803000",
        "status": "open",
    },
    {
        "name": "Katavi Regional Referral Hospital",
        "district": "Mpanda",
        "region": "Katavi",
        "address": "Mpanda, Katavi",
        "phone": "+255 26 2803000",
        "status": "open",
    },
]

def seed_hospitals():
    db = SessionLocal()
    try:
        # Clear existing hospitals
        db.query(Hospital).delete()
        
        # Add new hospitals
        for hospital_data in hospitals_data:
            # Add type based on hospital name
            hospital_data['type'] = get_hospital_type(hospital_data['name'])
            # Add zone based on region
            hospital_data['zone'] = get_zone(hospital_data['region'])
            hospital = Hospital(**hospital_data)
            db.add(hospital)
        
        db.commit()
        print("Successfully seeded hospitals data")
    except Exception as e:
        db.rollback()
        print(f"Error seeding hospitals: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_hospitals()
