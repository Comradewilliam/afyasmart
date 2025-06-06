package com.afyasmart;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;
import com.afyasmart.model.Hospital;
import java.util.List;

public class HospitalAdapter extends BaseAdapter {
    private Context context;
    private List<Hospital> hospitals;

    public HospitalAdapter(Context context, List<Hospital> hospitals) {
        this.context = context;
        this.hospitals = hospitals;
    }

    @Override
    public int getCount() {
        return hospitals.size();
    }

    @Override
    public Object getItem(int position) {
        return hospitals.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            convertView = LayoutInflater.from(context).inflate(R.layout.item_hospital, parent, false);
        }
        Hospital hospital = hospitals.get(position);
        ((TextView) convertView.findViewById(R.id.hospital_name)).setText(hospital.getName());
        ((TextView) convertView.findViewById(R.id.hospital_status)).setText(hospital.getStatus());
        ((TextView) convertView.findViewById(R.id.hospital_contact)).setText(hospital.getContact());
        ((TextView) convertView.findViewById(R.id.hospital_address)).setText(hospital.getAddress());
        ((TextView) convertView.findViewById(R.id.hospital_phone)).setText(hospital.getPhone());
        return convertView;
    }
}
