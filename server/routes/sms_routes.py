from flask import Blueprint, request, jsonify
from services.africa_talking import get_at_gateway
from database import get_db, User, SMSLog
import phonenumbers

bp = Blueprint('sms', __name__)

def register_sms_routes(app):
    app.register_blueprint(bp, url_prefix='/api/sms')

@bp.route('/send', methods=['POST'])
def send_sms():
    """Send SMS to one or more recipients"""
    data = request.json
    phone_numbers = data.get('phone_numbers', [])
    message = data.get('message')
    
    if not phone_numbers or not message:
        return jsonify({
            "status": "error",
            "message": "Phone numbers and message are required"
        }), 400
        
    # Validate phone numbers
    valid_numbers = []
    for number in phone_numbers:
        try:
            parsed = phonenumbers.parse(number, "TZ")
            if phonenumbers.is_valid_number(parsed):
                valid_numbers.append(phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.E164
                ))
        except Exception:
            continue
            
    if not valid_numbers:
        return jsonify({
            "status": "error",
            "message": "No valid phone numbers provided"
        }), 400
        
    # Send SMS
    at_gateway = get_at_gateway()
    response = at_gateway.send_sms(valid_numbers, message)
    
    # Log SMS if successful
    if response['status'] == 'success':
        db = next(get_db())
        try:
            for number in valid_numbers:
                # Get or create user
                user = db.query(User).filter(User.phone_number == number).first()
                if not user:
                    user = User(phone_number=number)
                    db.add(user)
                    db.flush()
                
                # Log SMS
                sms_log = SMSLog(
                    user_id=user.id,
                    message=message,
                    status=response['status']
                )
                db.add(sms_log)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error logging SMS: {str(e)}")
        finally:
            db.close()
    
    return jsonify(response)

@bp.route('/callback', methods=['POST'])
def sms_callback():
    """Handle SMS delivery reports"""
    data = request.json
    
    # Update SMS log status
    if data.get('phoneNumber') and data.get('status'):
        db = next(get_db())
        try:
            user = db.query(User)\
                .filter(User.phone_number == data['phoneNumber'])\
                .first()
                
            if user:
                sms_log = db.query(SMSLog)\
                    .filter(SMSLog.user_id == user.id)\
                    .order_by(SMSLog.created_at.desc())\
                    .first()
                    
                if sms_log:
                    sms_log.status = data['status']
                    db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error updating SMS log: {str(e)}")
        finally:
            db.close()
    
    return jsonify({
        "status": "success",
        "message": "Callback processed"
    })
