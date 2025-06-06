package com.afyasmart.network;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Headers;
import retrofit2.http.POST;

import java.util.Map;

public interface ApiService {
    @Headers("Content-Type: application/json")
    @POST("/api/chat")
    Call<Map<String, Object>> sendMessage(@Body Map<String, String> body);

    @retrofit2.http.GET("/api/hospitals")
    Call<java.util.List<com.afyasmart.model.Hospital>> getHospitals();

    @retrofit2.http.GET("/api/emergency-contacts")
    Call<java.util.List<com.afyasmart.model.EmergencyContact>> getEmergencyContacts();
}
