from flask import Blueprint, request, jsonify
from services.ai_service import get_ai_service
from database import get_db, User, AIConversation
from sqlalchemy.orm import Session

bp = Blueprint('ai', __name__)

def register_ai_routes(app):
    app.register_blueprint(bp, url_prefix='/api/ai')

@bp.route('/first-aid', methods=['POST'])
async def first_aid_guidance():
    """Get first aid guidance for a specific condition"""
    data = request.json
    condition = data.get('condition')
    language = data.get('language', 'en')
    
    if not condition:
        return jsonify({
            "status": "error",
            "message": "Condition is required"
        }), 400
        
    ai_service = get_ai_service()
    response = await ai_service.get_first_aid_guidance(condition, language)
    
    # Log the conversation if user_id is provided
    user_id = data.get('user_id')
    if user_id and response['status'] == 'success':
        db = next(get_db())
        try:
            conversation = AIConversation(
                user_id=user_id,
                message=condition,
                response=response['data']['guidance']
            )
            db.add(conversation)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error logging conversation: {str(e)}")
        finally:
            db.close()
    
    return jsonify(response)

@bp.route('/health-advice', methods=['POST'])
async def health_advice():
    """Get general health advice"""
    data = request.json
    query = data.get('query')
    language = data.get('language', 'en')
    
    if not query:
        return jsonify({
            "status": "error",
            "message": "Query is required"
        }), 400
        
    ai_service = get_ai_service()
    response = await ai_service.get_health_advice(query, language)
    
    # Log the conversation if user_id is provided
    user_id = data.get('user_id')
    if user_id and response['status'] == 'success':
        db = next(get_db())
        try:
            conversation = AIConversation(
                user_id=user_id,
                message=query,
                response=response['data']['advice']
            )
            db.add(conversation)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error logging conversation: {str(e)}")
        finally:
            db.close()
    
    return jsonify(response)

@bp.route('/conversation-history', methods=['GET'])
def conversation_history():
    """Get conversation history for a user"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "User ID is required"
        }), 400
        
    db = next(get_db())
    try:
        conversations = db.query(AIConversation)\
            .filter(AIConversation.user_id == user_id)\
            .order_by(AIConversation.created_at.desc())\
            .all()
            
        return jsonify({
            "status": "success",
            "message": "Conversation history retrieved successfully",
            "data": [
                {
                    "id": conv.id,
                    "message": conv.message,
                    "response": conv.response,
                    "created_at": conv.created_at.isoformat()
                }
                for conv in conversations
            ]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error retrieving conversation history: {str(e)}"
        }), 500
    finally:
        db.close()
