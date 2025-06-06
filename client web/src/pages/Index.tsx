
import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { MessageCircle, MapPin, Phone, Stethoscope } from 'lucide-react';
import { LanguageProvider, useLanguage } from '@/contexts/LanguageContext';
import LanguageSwitcher from '@/components/LanguageSwitcher';
import ChatBot from '@/components/ChatBot';
import HospitalSearch from '@/components/HospitalSearch';
import EmergencyContacts from '@/components/EmergencyContacts';

type ActiveTab = 'home' | 'chat' | 'hospitals' | 'emergency';

const AppContent = () => {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState<ActiveTab>('home');

  const renderContent = () => {
    switch (activeTab) {
      case 'chat':
        return (
          <Card className="h-full">
            <CardHeader className="border-b bg-health-50">
              <CardTitle className="flex items-center gap-2 text-health-800">
                <MessageCircle className="h-5 w-5" />
                {t.chat.title}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0 h-full">
              <ChatBot />
            </CardContent>
          </Card>
        );
      case 'hospitals':
        return (
          <Card>
            <CardHeader className="border-b bg-medical-50">
              <CardTitle className="flex items-center gap-2 text-medical-800">
                <MapPin className="h-5 w-5" />
                {t.hospitals.title}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <HospitalSearch />
            </CardContent>
          </Card>
        );
      case 'emergency':
        return (
          <Card>
            <CardHeader className="border-b bg-red-50">
              <CardTitle className="flex items-center gap-2 text-red-800">
                <Phone className="h-5 w-5" />
                {t.emergency.title}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <EmergencyContacts />
            </CardContent>
          </Card>
        );
      default:
        return (
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="text-center space-y-4 py-8">
              <div className="flex items-center justify-center gap-3 mb-4">
                <div className="bg-health-600 p-3 rounded-full">
                  <Stethoscope className="h-8 w-8 text-white" />
                </div>
                <div>
                  <h1 className="text-4xl font-bold text-gray-900">{t.app.title}</h1>
                  <p className="text-xl text-health-600 font-medium">{t.app.subtitle}</p>
                </div>
              </div>
              <p className="text-gray-600 max-w-2xl mx-auto">
                Access AI-powered health assistance, find nearby hospitals, and get emergency help. 
                Designed for rural Tanzania with mobile-first accessibility.
              </p>
            </div>

            {/* Feature Cards */}
            <div className="grid md:grid-cols-3 gap-6">
              <Card 
                className="hover:shadow-lg transition-all duration-200 cursor-pointer border-health-200 hover:border-health-400"
                onClick={() => setActiveTab('chat')}
              >
                <CardHeader className="text-center">
                  <div className="mx-auto bg-health-100 p-4 rounded-full w-fit mb-4">
                    <MessageCircle className="h-8 w-8 text-health-600" />
                  </div>
                  <CardTitle className="text-health-800">{t.navigation.chat}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 text-center">
                    Get instant health guidance from our AI assistant. Ask questions about symptoms, 
                    first aid, and general health advice.
                  </p>
                </CardContent>
              </Card>

              <Card 
                className="hover:shadow-lg transition-all duration-200 cursor-pointer border-medical-200 hover:border-medical-400"
                onClick={() => setActiveTab('hospitals')}
              >
                <CardHeader className="text-center">
                  <div className="mx-auto bg-medical-100 p-4 rounded-full w-fit mb-4">
                    <MapPin className="h-8 w-8 text-medical-600" />
                  </div>
                  <CardTitle className="text-medical-800">{t.navigation.hospitals}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 text-center">
                    Find nearby hospitals and healthcare facilities. Search by location or use GPS 
                    to discover the closest medical services.
                  </p>
                </CardContent>
              </Card>

              <Card 
                className="hover:shadow-lg transition-all duration-200 cursor-pointer border-red-200 hover:border-red-400"
                onClick={() => setActiveTab('emergency')}
              >
                <CardHeader className="text-center">
                  <div className="mx-auto bg-red-100 p-4 rounded-full w-fit mb-4">
                    <Phone className="h-8 w-8 text-red-600" />
                  </div>
                  <CardTitle className="text-red-800">{t.navigation.emergency}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 text-center">
                    Quick access to emergency services. Call ambulance, police, or fire department 
                    with one tap for immediate assistance.
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Quick Stats */}
            <div className="bg-gradient-to-r from-health-50 to-medical-50 rounded-lg p-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div>
                  <p className="text-2xl font-bold text-health-600">24/7</p>
                  <p className="text-sm text-gray-600">AI Assistant</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-medical-600">500+</p>
                  <p className="text-sm text-gray-600">Hospitals Listed</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-health-600">2</p>
                  <p className="text-sm text-gray-600">Languages</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-red-600">3</p>
                  <p className="text-sm text-gray-600">Emergency Lines</p>
                </div>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-health-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-health-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <Button
                variant="ghost"
                onClick={() => setActiveTab('home')}
                className="text-health-700 hover:text-health-800 hover:bg-health-50"
              >
                <Stethoscope className="h-5 w-5 mr-2" />
                {t.app.title}
              </Button>
            </div>
            
            <div className="flex items-center gap-4">
              {/* Navigation */}
              <nav className="hidden md:flex items-center gap-2">
                <Button
                  variant={activeTab === 'chat' ? 'default' : 'ghost'}
                  onClick={() => setActiveTab('chat')}
                  className={activeTab === 'chat' ? 'bg-health-600 hover:bg-health-700' : 'hover:bg-health-50'}
                >
                  <MessageCircle className="h-4 w-4 mr-2" />
                  {t.navigation.chat}
                </Button>
                <Button
                  variant={activeTab === 'hospitals' ? 'default' : 'ghost'}
                  onClick={() => setActiveTab('hospitals')}
                  className={activeTab === 'hospitals' ? 'bg-medical-600 hover:bg-medical-700' : 'hover:bg-medical-50'}
                >
                  <MapPin className="h-4 w-4 mr-2" />
                  {t.navigation.hospitals}
                </Button>
                <Button
                  variant={activeTab === 'emergency' ? 'default' : 'ghost'}
                  onClick={() => setActiveTab('emergency')}
                  className={activeTab === 'emergency' ? 'bg-red-600 hover:bg-red-700' : 'hover:bg-red-50'}
                >
                  <Phone className="h-4 w-4 mr-2" />
                  {t.navigation.emergency}
                </Button>
              </nav>
              
              <LanguageSwitcher />
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Navigation */}
      <div className="md:hidden bg-white border-b border-health-100 px-4 py-2">
        <div className="flex gap-2 overflow-x-auto">
          <Button
            variant={activeTab === 'home' ? 'default' : 'ghost'}
            onClick={() => setActiveTab('home')}
            size="sm"
            className={activeTab === 'home' ? 'bg-health-600 hover:bg-health-700' : 'hover:bg-health-50'}
          >
            Home
          </Button>
          <Button
            variant={activeTab === 'chat' ? 'default' : 'ghost'}
            onClick={() => setActiveTab('chat')}
            size="sm"
            className={activeTab === 'chat' ? 'bg-health-600 hover:bg-health-700' : 'hover:bg-health-50'}
          >
            <MessageCircle className="h-4 w-4 mr-1" />
            AI
          </Button>
          <Button
            variant={activeTab === 'hospitals' ? 'default' : 'ghost'}
            onClick={() => setActiveTab('hospitals')}
            size="sm"
            className={activeTab === 'hospitals' ? 'bg-medical-600 hover:bg-medical-700' : 'hover:bg-medical-50'}
          >
            <MapPin className="h-4 w-4 mr-1" />
            Hospitals
          </Button>
          <Button
            variant={activeTab === 'emergency' ? 'default' : 'ghost'}
            onClick={() => setActiveTab('emergency')}
            size="sm"
            className={activeTab === 'emergency' ? 'bg-red-600 hover:bg-red-700' : 'hover:bg-red-50'}
          >
            <Phone className="h-4 w-4 mr-1" />
            Emergency
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderContent()}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Stethoscope className="h-6 w-6 text-health-400" />
            <span className="text-xl font-bold">{t.app.title}</span>
          </div>
          <p className="text-gray-400 mb-4">
            Democratizing healthcare access in rural Tanzania through technology
          </p>
          <p className="text-sm text-gray-500">
            © 2024 AfyaSmart. Built with ❤️ for Tanzania's health.
          </p>
        </div>
      </footer>
    </div>
  );
};

const Index = () => {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  );
};

export default Index;
