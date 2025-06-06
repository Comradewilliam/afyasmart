from flask import Blueprint, request, jsonify
from services.africa_talking import AfricaTalkingGateway
from database import get_db, Hospital
from sqlalchemy import distinct

bp = Blueprint('voice', __name__)
at_gateway = AfricaTalkingGateway()

def register_voice_routes(app):
    app.register_blueprint(bp, url_prefix='/api/voice')

def get_zones(db):
    return [z[0] for z in db.query(distinct(Hospital.zone)).all()]

def get_regions(db, zone):
    return [r[0] for r in db.query(distinct(Hospital.region)).filter(Hospital.zone == zone).all()]

def get_districts(db, region):
    return [d[0] for d in db.query(distinct(Hospital.district)).filter(Hospital.region == region).all()]

def get_facilities(db, district):
    return db.query(Hospital).filter(Hospital.district == district).all()

def create_voice_response(text_en, text_sw):
    """Create voice response in both languages"""
    response = "<?xml version='1.0' encoding='UTF-8'?><Response>"
    response += f"<Say voice='en'>{text_en}</Say>"
    response += f"<Say voice='sw'>{text_sw}</Say>"
    response += "</Response>"
    return response

@bp.route('/call', methods=['POST'])
def initiate_call():
    """Initiate a voice call"""
    data = request.json
    phone_number = data.get('phone_number')
    callback_url = data.get('callback_url')
    
    if not phone_number:
        return jsonify({"status": "error", "message": "Phone number required"})
        
    try:
        result = at_service.make_call(phone_number, callback_url)
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@bp.route('/callback', methods=['POST'])
def voice_callback():
    """Handle voice call events"""
    session_id = request.form.get('sessionId')
    caller_number = request.form.get('callerNumber')
    
    try:
        # Initial menu
        response = "<?xml version='1.0' encoding='UTF-8'?><Response>"
        response += "<GetDigits timeout='30' finishOnKey='#' callbackUrl='/voice/menu'>"
        response += "<Say voice='en'>Welcome to AfyaSmart. Press 1 to find hospitals, 2 for emergency services.</Say>"
        response += "<Say voice='sw'>Karibu AfyaSmart. Bonyeza 1 kutafuta hospitali, 2 kwa huduma za dharura.</Say>"
        response += "</GetDigits></Response>"
        return response
    except Exception as e:
        return str(e)

@bp.route('/menu', methods=['POST'])
def voice_menu():
    """Handle DTMF input for voice menu"""
    session_id = request.form.get('sessionId')
    digits = request.form.get('dtmfDigits')
    menu_level = request.form.get('menuLevel', '0')
    selected_zone = request.form.get('selectedZone', '')
    selected_region = request.form.get('selectedRegion', '')
    
    db = next(get_db())
    try:
        if digits == '1':  # Find hospitals
            if menu_level == '0':
                # List zones
                zones = get_zones(db)
                response = "<?xml version='1.0' encoding='UTF-8'?><Response>"
                response += "<GetDigits timeout='30' finishOnKey='#' callbackUrl='/voice/menu?menuLevel=1'>"
                response += "<Say voice='en'>Select zone:</Say>"
                response += "<Say voice='sw'>Chagua eneo:</Say>"
                for i, zone in enumerate(zones, 1):
                    response += f"<Say voice='en'>{i} for {zone}</Say>"
                    response += f"<Say voice='sw'>{i} kwa {zone}</Say>"
                response += "</GetDigits></Response>"
                
            elif menu_level == '1':
                # List regions in selected zone
                zones = get_zones(db)
                selected_zone = zones[int(digits) - 1]
                regions = get_regions(db, selected_zone)
                
                response = "<?xml version='1.0' encoding='UTF-8'?><Response>"
                response += f"<GetDigits timeout='30' finishOnKey='#' callbackUrl='/voice/menu?menuLevel=2&selectedZone={selected_zone}'>"
                response += f"<Say voice='en'>Select region in {selected_zone}:</Say>"
                response += f"<Say voice='sw'>Chagua mkoa katika {selected_zone}:</Say>"
                for i, region in enumerate(regions, 1):
                    response += f"<Say voice='en'>{i} for {region}</Say>"
                    response += f"<Say voice='sw'>{i} kwa {region}</Say>"
                response += "</GetDigits></Response>"
                
            elif menu_level == '2':
                # List districts in selected region
                regions = get_regions(db, selected_zone)
                selected_region = regions[int(digits) - 1]
                districts = get_districts(db, selected_region)
                
                response = "<?xml version='1.0' encoding='UTF-8'?><Response>"
                response += f"<GetDigits timeout='30' finishOnKey='#' callbackUrl='/voice/menu?menuLevel=3&selectedZone={selected_zone}&selectedRegion={selected_region}'>"
                response += f"<Say voice='en'>Select district in {selected_region}:</Say>"
                response += f"<Say voice='sw'>Chagua wilaya katika {selected_region}:</Say>"
                for i, district in enumerate(districts, 1):
                    response += f"<Say voice='en'>{i} for {district}</Say>"
                    response += f"<Say voice='sw'>{i} kwa {district}</Say>"
                response += "</GetDigits></Response>"
                
            elif menu_level == '3':
                # List facilities in selected district
                districts = get_districts(db, selected_region)
                selected_district = districts[int(digits) - 1]
                facilities = get_facilities(db, selected_district)
                
                response = "<?xml version='1.0' encoding='UTF-8'?><Response>"
                for facility in facilities:
                    response += f"<Say voice='en'>{facility.name}, {facility.type}. Phone: {facility.phone}</Say>"
                    response += f"<Say voice='sw'>{facility.name}, {facility.type}. Simu: {facility.phone}</Say>"
                response += "<Say voice='en'>End of list. Thank you for using AfyaSmart.</Say>"
                response += "<Say voice='sw'>Mwisho wa orodha. Asante kwa kutumia AfyaSmart.</Say>"
                response += "</Response>"
                
        elif digits == '2':  # Emergency services
            response = "<?xml version='1.0' encoding='UTF-8'?><Response>"
            response += "<GetDigits timeout='30' finishOnKey='#'>"
            response += "<Say voice='en'>Press 1 for ambulance, 2 for police, 3 for fire department.</Say>"
            response += "<Say voice='sw'>Bonyeza 1 kwa ambulance, 2 kwa polisi, 3 kwa zimamoto.</Say>"
            response += "</GetDigits>"
            
            if digits == '1':
                response += "<Say voice='en'>Connecting to ambulance services.</Say>"
                response += "<Say voice='sw'>Tunakuunganisha na huduma za ambulance.</Say>"
                response += "<Dial phoneNumbers='+255115'/>"
            elif digits == '2':
                response += "<Say voice='en'>Connecting to police services.</Say>"
                response += "<Say voice='sw'>Tunakuunganisha na huduma za polisi.</Say>"
                response += "<Dial phoneNumbers='+255112'/>"
            elif digits == '3':
                response += "<Say voice='en'>Connecting to fire department.</Say>"
                response += "<Say voice='sw'>Tunakuunganisha na huduma za zimamoto.</Say>"
                response += "<Dial phoneNumbers='+255114'/>"
                
            response += "</Response>"
            
        else:
            response = create_voice_response(
                "Invalid selection. Please try again.",
                "Chaguo sio sahihi. Tafadhali jaribu tena."
            )
            
        return response
        
    except Exception as e:
        return create_voice_response(
            f"An error occurred: {str(e)}",
            f"Hitilafu imetokea: {str(e)}"
        )
    finally:
        db.close()
