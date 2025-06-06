from flask_restx import Api, Resource, fields

# Create API documentation instance
api = Api(
    title='AfyaSmart API',
    version='1.0',
    description='AfyaSmart Healthcare API Documentation',
    doc='/api/docs'
)

# Define namespaces
hospitals_ns = api.namespace('hospitals', description='Hospital operations')
ai_ns = api.namespace('ai', description='AI assistant operations')
sms_ns = api.namespace('sms', description='SMS operations')
ussd_ns = api.namespace('ussd', description='USSD operations')
voice_ns = api.namespace('voice', description='Voice operations')

# Define models
hospital = api.model('Hospital', {
    'name': fields.String(required=True, description='Hospital name'),
    'type': fields.String(required=True, description='Facility type (Hospital, Clinic, Health Center)'),
    'zone': fields.String(required=True, description='Geographical zone'),
    'region': fields.String(required=True, description='Region'),
    'district': fields.String(required=True, description='District'),
    'phone': fields.String(required=True, description='Contact phone number'),
    'email': fields.String(required=True, description='Contact email'),
    'address': fields.String(required=True, description='Physical address'),
    'services': fields.String(required=True, description='Available services')
})

ai_request = api.model('AIRequest', {
    'query': fields.String(required=True, description='User query'),
    'language': fields.String(required=True, description='Response language (en/sw)')
})

sms_request = api.model('SMSRequest', {
    'phone_numbers': fields.List(fields.String, required=True, description='List of recipient phone numbers'),
    'message': fields.String(required=True, description='SMS message content')
})

ussd_request = api.model('USSDRequest', {
    'sessionId': fields.String(required=True, description='USSD session ID'),
    'phoneNumber': fields.String(required=True, description='User phone number'),
    'text': fields.String(required=True, description='USSD input text')
})

voice_request = api.model('VoiceRequest', {
    'phone_number': fields.String(required=True, description='Caller phone number')
})
