from flask import Blueprint, request, jsonify
from database import get_db, Hospital
from sqlalchemy import or_
from geopy.distance import geodesic

bp = Blueprint('hospitals', __name__)

def register_hospital_routes(app):
    app.register_blueprint(bp, url_prefix='/api/hospitals')

@bp.route('/', methods=['GET'])
def get_hospitals():
    """Get list of hospitals with optional filtering"""
    zone = request.args.get('zone')
    region = request.args.get('region')
    district = request.args.get('district')
    search = request.args.get('search')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    
    db = next(get_db())
    try:
        query = db.query(Hospital)
        
        # Apply filters
        if zone:
            query = query.filter(Hospital.zone == zone)
        if region:
            query = query.filter(Hospital.region == region)
        if district:
            query = query.filter(Hospital.district == district)
        if search:
            search_filter = or_(
                Hospital.name.ilike(f'%{search}%'),
                Hospital.address.ilike(f'%{search}%'),
                Hospital.services.ilike(f'%{search}%')
            )
            query = query.filter(search_filter)
            
        hospitals = query.all()
        
        # Calculate distances if coordinates provided
        if lat is not None and lng is not None:
            user_location = (lat, lng)
            for hospital in hospitals:
                if hospital.latitude and hospital.longitude:
                    hospital_location = (hospital.latitude, hospital.longitude)
                    distance = geodesic(user_location, hospital_location).kilometers
                    hospital.distance = round(distance, 2)
                else:
                    hospital.distance = None
            
            # Sort by distance
            hospitals.sort(key=lambda h: h.distance if h.distance is not None else float('inf'))
        
        return jsonify({
            "status": "success",
            "message": "Hospitals retrieved successfully",
            "data": [
                {
                    "id": h.id,
                    "name": h.name,
                    "zone": h.zone,
                    "region": h.region,
                    "district": h.district,
                    "latitude": h.latitude,
                    "longitude": h.longitude,
                    "phone": h.phone,
                    "email": h.email,
                    "address": h.address,
                    "services": h.services.split(',') if h.services else [],
                    "distance": h.distance if hasattr(h, 'distance') else None
                }
                for h in hospitals
            ]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error retrieving hospitals: {str(e)}"
        }), 500
    finally:
        db.close()

@bp.route('/<int:hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    """Get hospital details by ID"""
    db = next(get_db())
    try:
        hospital = db.query(Hospital).get(hospital_id)
        
        if not hospital:
            return jsonify({
                "status": "error",
                "message": "Hospital not found"
            }), 404
            
        return jsonify({
            "status": "success",
            "message": "Hospital retrieved successfully",
            "data": {
                "id": hospital.id,
                "name": hospital.name,
                "zone": hospital.zone,
                "region": hospital.region,
                "district": hospital.district,
                "latitude": hospital.latitude,
                "longitude": hospital.longitude,
                "phone": hospital.phone,
                "email": hospital.email,
                "address": hospital.address,
                "services": hospital.services.split(',') if hospital.services else []
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error retrieving hospital: {str(e)}"
        }), 500
    finally:
        db.close()

@bp.route('/zones', methods=['GET'])
def get_zones():
    """Get list of unique zones"""
    db = next(get_db())
    try:
        zones = db.query(Hospital.zone)\
            .distinct()\
            .filter(Hospital.zone.isnot(None))\
            .all()
            
        return jsonify({
            "status": "success",
            "message": "Zones retrieved successfully",
            "data": [zone[0] for zone in zones]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error retrieving zones: {str(e)}"
        }), 500
    finally:
        db.close()

@bp.route('/regions', methods=['GET'])
def get_regions():
    """Get list of regions, optionally filtered by zone"""
    zone = request.args.get('zone')
    
    db = next(get_db())
    try:
        query = db.query(Hospital.region)\
            .distinct()\
            .filter(Hospital.region.isnot(None))
            
        if zone:
            query = query.filter(Hospital.zone == zone)
            
        regions = query.all()
            
        return jsonify({
            "status": "success",
            "message": "Regions retrieved successfully",
            "data": [region[0] for region in regions]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error retrieving regions: {str(e)}"
        }), 500
    finally:
        db.close()

@bp.route('/districts', methods=['GET'])
def get_districts():
    """Get list of districts, optionally filtered by region"""
    region = request.args.get('region')
    
    db = next(get_db())
    try:
        query = db.query(Hospital.district)\
            .distinct()\
            .filter(Hospital.district.isnot(None))
            
        if region:
            query = query.filter(Hospital.region == region)
            
        districts = query.all()
            
        return jsonify({
            "status": "success",
            "message": "Districts retrieved successfully",
            "data": [district[0] for district in districts]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error retrieving districts: {str(e)}"
        }), 500
    finally:
        db.close()
