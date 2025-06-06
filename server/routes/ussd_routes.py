from flask import Blueprint, request, jsonify
from services.africa_talking import AfricaTalkingGateway
from database import get_db, Hospital
from sqlalchemy import distinct

bp = Blueprint('ussd', __name__)
at_gateway = AfricaTalkingGateway()

def register_ussd_routes(app):
    app.register_blueprint(bp, url_prefix='/api/ussd')

def get_zones(db):
    return [z[0] for z in db.query(distinct(Hospital.zone)).all()]

def get_regions(db, zone):
    return [r[0] for r in db.query(distinct(Hospital.region)).filter(Hospital.zone == zone).all()]

def get_districts(db, region):
    return [d[0] for d in db.query(distinct(Hospital.district)).filter(Hospital.region == region).all()]

def get_facilities(db, district):
    return db.query(Hospital).filter(Hospital.district == district).all()

@bp.route('/callback', methods=['POST'])
def ussd_callback():
    """Handle USSD session"""
    session_id = request.form.get('sessionId')
    phone_number = request.form.get('phoneNumber')
    text = request.form.get('text', '')
    
    db = next(get_db())
    try:
        # Split input into parts
        parts = text.split('*')
        level = len(parts)
        
        # Main menu
        if text == '':
            response = "CON Karibu AfyaSmart\n"
            response += "1. Tafuta hospitali\n"
            response += "2. Namba za dharura\n"
            response += "3. Msaada wa kwanza"
            
        # Level 1 - Main menu selection
        elif level == 1:
            if parts[0] == '1':  # Find hospitals
                zones = get_zones(db)
                response = "CON Chagua eneo:\n"
                for i, zone in enumerate(zones, 1):
                    response += f"{i}. {zone}\n"
                    
            elif parts[0] == '2':  # Emergency
                response = "END Namba za dharura:\n"
                response += "Polisi: 112\n"
                response += "Ambulance: 115\n"
                response += "Zimamoto: 114"
                
            elif parts[0] == '3':  # First aid
                response = "CON Chagua hali:\n"
                response += "1. Kutoka damu\n"
                response += "2. Kuungua\n"
                response += "3. Kunyongwa\n"
                response += "4. Shambulio la moyo"
            else:
                response = "END Chaguo sio sahihi"
                
        # Level 2 - Zone selection
        elif level == 2 and parts[0] == '1':
            zones = get_zones(db)
            selected_zone = zones[int(parts[1]) - 1]
            regions = get_regions(db, selected_zone)
            
            response = f"CON Chagua mkoa ({selected_zone}):\n"
            for i, region in enumerate(regions, 1):
                response += f"{i}. {region}\n"
                
        # Level 3 - Region selection
        elif level == 3 and parts[0] == '1':
            zones = get_zones(db)
            selected_zone = zones[int(parts[1]) - 1]
            regions = get_regions(db, selected_zone)
            selected_region = regions[int(parts[2]) - 1]
            districts = get_districts(db, selected_region)
            
            response = f"CON Chagua wilaya ({selected_region}):\n"
            for i, district in enumerate(districts, 1):
                response += f"{i}. {district}\n"
                
        # Level 4 - District selection
        elif level == 4 and parts[0] == '1':
            zones = get_zones(db)
            selected_zone = zones[int(parts[1]) - 1]
            regions = get_regions(db, selected_zone)
            selected_region = regions[int(parts[2]) - 1]
            districts = get_districts(db, selected_region)
            selected_district = districts[int(parts[3]) - 1]
            facilities = get_facilities(db, selected_district)
            
            response = f"END Vituo vya afya ({selected_district}):\n\n"
            for facility in facilities:
                response += f"{facility.name} ({facility.type})\n"
                response += f"Simu: {facility.phone}\n"
                response += f"Anwani: {facility.address}\n\n"
            
        else:
            response = "END Chaguo sio sahihi"
            
        return response
        
    except Exception as e:
        return f"END Hitilafu: {str(e)}"
    finally:
        db.close()

@bp.route('/hospitals', methods=['POST'])
def get_hospitals_ussd():
    """Get hospitals list for USSD"""
    data = request.json
    zone = data.get('zone')
    region = data.get('region')
    district = data.get('district')
    
    db = next(get_db())
    try:
        query = db.query(Hospital)
        
        if zone:
            query = query.filter(Hospital.zone == zone)
        if region:
            query = query.filter(Hospital.region == region)
        if district:
            query = query.filter(Hospital.district == district)
            
        hospitals = query.all()
        return jsonify({
            "status": "success",
            "data": [{
                "id": h.id,
                "name": h.name,
                "type": h.type,
                "address": h.address,
                "phone": h.phone
            } for h in hospitals]
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        db.close()

@bp.route('/hospital/<int:hospital_id>', methods=['POST'])
def get_hospital_details_ussd():
    """Get hospital details for USSD"""
    data = request.json
    hospital_id = data.get('hospital_id')
    
    if not hospital_id:
        return "END Hospital ID is required."
        
    db = next(get_db())
    try:
        hospital = db.query(Hospital).get(hospital_id)
        
        if not hospital:
            return "END Hospital not found."
            
        response = f"END {hospital.name}\n"
        if hospital.address:
            response += f"Address: {hospital.address}\n"
        if hospital.phone:
            response += f"Phone: {hospital.phone}\n"
        if hospital.services:
            response += f"Services: {hospital.services}"
            
        return response
        
    except Exception as e:
        print(f"Error retrieving hospital: {str(e)}")
        return "END An error occurred. Please try again."
    finally:
        db.close()
