package com.afyasmart.model;

public class Hospital {
    private String name;
    private String status;
    private String contact;
    private String address;
    private String phone;

    public Hospital(String name, String status, String contact, String address, String phone) {
        this.name = name;
        this.status = status;
        this.contact = contact;
        this.address = address;
        this.phone = phone;
    }

    public String getName() { return name; }
    public String getStatus() { return status; }
    public String getContact() { return contact; }
    public String getAddress() { return address; }
    public String getPhone() { return phone; }
}
