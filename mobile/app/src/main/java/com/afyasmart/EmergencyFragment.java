package com.afyasmart;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.Fragment;
import com.afyasmart.model.EmergencyContact;
import com.afyasmart.network.ApiClient;
import com.afyasmart.network.ApiService;
import java.util.ArrayList;
import java.util.List;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class EmergencyFragment extends Fragment {
    private static final int REQUEST_CALL_PHONE = 1;
    private ListView contactsListView;
    private ProgressBar progressBar;
    private EmergencyContactAdapter contactAdapter;
    private List<EmergencyContact> contacts = new ArrayList<>();
    private String pendingPhoneNumber = null;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_emergency, container, false);
        contactsListView = view.findViewById(R.id.contacts_list);
        progressBar = view.findViewById(R.id.progress_bar);
        contactAdapter = new EmergencyContactAdapter(getContext(), contacts);
        contactsListView.setAdapter(contactAdapter);
        fetchContacts();
        contactsListView.setOnItemClickListener((AdapterView<?> parent, View v, int position, long id) -> {
            EmergencyContact contact = contacts.get(position);
            String phone = contact.getPhone();
            if (ActivityCompat.checkSelfPermission(getContext(), Manifest.permission.CALL_PHONE) == PackageManager.PERMISSION_GRANTED) {
                startCall(phone);
            } else {
                pendingPhoneNumber = phone;
                requestPermissions(new String[]{Manifest.permission.CALL_PHONE}, REQUEST_CALL_PHONE);
            }
        });
        return view;
    }

    private void startCall(String phone) {
        Intent intent = new Intent(Intent.ACTION_CALL);
        intent.setData(Uri.parse("tel:" + phone));
        startActivity(intent);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_CALL_PHONE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED && pendingPhoneNumber != null) {
                startCall(pendingPhoneNumber);
            } else {
                Toast.makeText(getContext(), getString(R.string.emergency_error), Toast.LENGTH_SHORT).show();
            }
            pendingPhoneNumber = null;
        }
    }

    private void fetchContacts() {
        progressBar.setVisibility(View.VISIBLE);
        ApiService apiService = ApiClient.getClient().create(ApiService.class);
        apiService.getEmergencyContacts().enqueue(new Callback<List<EmergencyContact>>() {
            @Override
            public void onResponse(Call<List<EmergencyContact>> call, Response<List<EmergencyContact>> response) {
                progressBar.setVisibility(View.GONE);
                if (response.isSuccessful() && response.body() != null) {
                    contacts.clear();
                    contacts.addAll(response.body());
                    contactAdapter.notifyDataSetChanged();
                } else {
                    Toast.makeText(getContext(), getString(R.string.app_error), Toast.LENGTH_SHORT).show();
                }
            }
            @Override
            public void onFailure(Call<List<EmergencyContact>> call, Throwable t) {
                progressBar.setVisibility(View.GONE);
                Toast.makeText(getContext(), getString(R.string.app_error), Toast.LENGTH_SHORT).show();
            }
        });
    }
}
