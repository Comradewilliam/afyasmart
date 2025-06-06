
import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Phone, Truck, Shield, Flame } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

interface EmergencyContact {
  id: string;
  name: string;
  number: string;
  icon: React.ReactNode;
  color: string;
}

const EmergencyContacts = () => {
  const { t } = useLanguage();

  const emergencyContacts: EmergencyContact[] = [
    {
      id: '1',
      name: t.emergency.ambulance,
      number: '114',
      icon: <Truck className="h-6 w-6" />,
      color: 'bg-health-600 hover:bg-health-700',
    },
    {
      id: '2',
      name: t.emergency.police,
      number: '112',
      icon: <Shield className="h-6 w-6" />,
      color: 'bg-blue-600 hover:bg-blue-700',
    },
    {
      id: '3',
      name: t.emergency.fire,
      number: '115',
      icon: <Flame className="h-6 w-6" />,
      color: 'bg-red-600 hover:bg-red-700',
    },
  ];

  const handleCall = (number: string) => {
    window.open(`tel:${number}`, '_self');
  };

  return (
    <div className="space-y-6">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-bold text-gray-900">{t.emergency.title}</h2>
        <p className="text-gray-600">Emergency services available 24/7</p>
      </div>

      <div className="grid gap-4">
        {emergencyContacts.map((contact) => (
          <Card key={contact.id} className="hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`p-3 rounded-full text-white ${contact.color.split(' ')[0]}`}>
                    {contact.icon}
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">{contact.name}</h3>
                    <p className="text-2xl font-bold text-gray-700">{contact.number}</p>
                  </div>
                </div>
                <Button
                  onClick={() => handleCall(contact.number)}
                  className={`${contact.color} text-white`}
                  size="lg"
                >
                  <Phone className="h-5 w-5 mr-2" />
                  {t.emergency.call}
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="bg-yellow-50 border-yellow-200">
        <CardContent className="p-4">
          <p className="text-sm text-yellow-800 text-center">
            <strong>Important:</strong> These services are for genuine emergencies only. 
            Misuse may result in delays for real emergency cases.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default EmergencyContacts;
