import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { MapPin, Phone, Navigation, Clock, Globe } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

interface Hospital {
  id: string;
  name: string;
  district: string;
  region: string;
  address: string;
  phone: string;
  website?: string | null;
  distance?: number | null;
  status: 'open' | 'closed';
}

const HospitalSearch = () => {
  const { t } = useLanguage();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('all');
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [filteredHospitals, setFilteredHospitals] = useState<Hospital[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch hospitals from backend API
  useEffect(() => {
    const fetchHospitals = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const res = await fetch('/api/hospitals/');
        if (!res.ok) throw new Error('Failed to fetch hospitals');
        const data = await res.json();
        setHospitals(data.data || []);
        setFilteredHospitals(data.data || []);
      } catch (err: any) {
        setError(err.message || 'Unknown error');
      } finally {
        setIsLoading(false);
      }
    };
    fetchHospitals();
  }, []);

  // Get unique regions from fetched hospitals
  const regions = Array.from(new Set(hospitals.map(h => h.region))).sort();

  // Filtering logic
  useEffect(() => {
    let filtered = hospitals;
    if (selectedRegion !== 'all') {
      filtered = filtered.filter(hospital => hospital.region === selectedRegion);
    }
    if (searchTerm) {
      filtered = filtered.filter(
        hospital =>
          hospital.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          hospital.district.toLowerCase().includes(searchTerm.toLowerCase()) ||
          hospital.region.toLowerCase().includes(searchTerm.toLowerCase()) ||
          hospital.address.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    setFilteredHospitals(filtered);
  }, [searchTerm, selectedRegion, hospitals]);

  const handleSearch = (term: string) => {
    setSearchTerm(term);
  };

  const handleRegionFilter = (region: string) => {
    setSelectedRegion(region);
  };


  const handleUseLocation = () => {
    setIsLoading(true);
    // Simulate geolocation API call
    setTimeout(() => {
      setIsLoading(false);
      // Sort by distance
      const sortedHospitals = [...hospitals].sort((a, b) => (a.distance || 0) - (b.distance || 0));
      setHospitals(sortedHospitals);
    }, 1500);
  };

  return (
    <div className="hospital-search-container">
      <Card className="mb-4">
        <CardHeader className="border-b bg-medical-50">
          <CardTitle className="flex items-center gap-2 text-medical-800">
            <MapPin className="h-5 w-5" />
            {t.hospitals.title}
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-4 flex flex-col gap-4">
          <div className="flex gap-2">
            <Input
              value={searchTerm}
              onChange={e => handleSearch(e.target.value)}
              placeholder={t.hospitals.searchPlaceholder}
              className="flex-1 border-medical-200 focus:border-medical-500 focus:ring-medical-500"
            />
            <Select value={selectedRegion} onValueChange={handleRegionFilter}>
              <SelectTrigger className="w-48 border-medical-200">
                <SelectValue placeholder="All Regions" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Regions</SelectItem>
                {regions.map(region => (
                  <SelectItem key={region} value={region}>{region}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {isLoading ? (
        <Card className="text-center py-8">
          <CardContent>
            <p className="text-gray-500">{t.common.loading}</p>
          </CardContent>
        </Card>
      ) : error ? (
        <Card className="text-center py-8">
          <CardContent>
            <p className="text-red-500">{t.common.error}: {error}</p>
            <Button onClick={() => window.location.reload()}>{t.common.retry}</Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredHospitals.length === 0 ? (
            <Card className="text-center py-8">
              <CardContent>
                <p className="text-gray-500">{t.hospitals.noResults}</p>
              </CardContent>
            </Card>
          ) : (
            filteredHospitals.map(hospital => (
              <Card key={hospital.id} className="hover:shadow-md transition-all duration-200">
                <CardHeader className="flex flex-row items-center justify-between border-b">
                  <div>
                    <CardTitle className="text-lg text-medical-700">{hospital.name}</CardTitle>
                    <div className="text-sm text-gray-500">
                      {hospital.district}, {hospital.region}
                    </div>
                    <div className="text-xs text-gray-400">{hospital.address}</div>
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    <div className="flex items-center gap-1 text-medical-600">
                      <Phone className="h-4 w-4 mr-1" />
                      <span>{hospital.phone}</span>
                    </div>
                    {hospital.distance !== undefined && hospital.distance !== null && (
                      <div className="flex items-center gap-1 text-xs text-gray-400">
                        <Navigation className="h-3 w-3 mr-1" />
                        {hospital.distance} {t.hospitals.distance}
                      </div>
                    )}
                    <div
                      className={`px-2 py-1 rounded text-xs font-semibold mt-2
                        ${
                          hospital.status === 'open' 
                            ? 'bg-health-100 text-health-700' 
                            : 'bg-red-100 text-red-700'
                        }
                      `}
                    >
                      <Clock className="h-3 w-3" />
                      {hospital.status === 'open' ? 'Open' : 'Closed'}
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <div className="space-y-3">
                    <div className="flex items-center gap-1 text-medical-600">
                      <Phone className="h-4 w-4 mr-1" />
                      <span>{hospital.phone}</span>
                    </div>
                    <Button
                      size="sm"
                      className="bg-health-600 hover:bg-health-700 text-white"
                      onClick={() => window.open(`tel:${hospital.phone}`, '_self')}
                    >
                      {t.emergency.call}
                    </Button>
                    {hospital.website && (
                      <div className="flex items-center text-sm text-gray-600">
                        <Globe className="h-4 w-4 mr-1" />
                        <a 
                          href={`https://${hospital.website}`} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-health-600 hover:text-health-700 underline"
                        >
                          {hospital.website}
                        </a>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default HospitalSearch;
