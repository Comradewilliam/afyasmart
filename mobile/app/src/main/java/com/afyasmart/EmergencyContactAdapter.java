package com.afyasmart;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;
import com.afyasmart.model.EmergencyContact;
import java.util.List;

public class EmergencyContactAdapter extends BaseAdapter {
    private Context context;
    private List<EmergencyContact> contacts;

    public EmergencyContactAdapter(Context context, List<EmergencyContact> contacts) {
        this.context = context;
        this.contacts = contacts;
    }

    @Override
    public int getCount() {
        return contacts.size();
    }

    @Override
    public Object getItem(int position) {
        return contacts.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            convertView = LayoutInflater.from(context).inflate(R.layout.item_emergency_contact, parent, false);
        }
        EmergencyContact contact = contacts.get(position);
        ((TextView) convertView.findViewById(R.id.contact_name)).setText(contact.getName());
        ((TextView) convertView.findViewById(R.id.contact_phone)).setText(contact.getPhone());
        return convertView;
    }
}
