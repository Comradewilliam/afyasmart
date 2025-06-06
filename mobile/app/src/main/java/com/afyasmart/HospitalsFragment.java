package com.afyasmart;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import com.afyasmart.model.Hospital;
import com.afyasmart.network.ApiClient;
import com.afyasmart.network.ApiService;
import java.util.ArrayList;
import java.util.List;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class HospitalsFragment extends Fragment {
    private ListView hospitalsListView;
    private EditText searchInput;
    private ProgressBar progressBar;
    private HospitalAdapter hospitalAdapter;
    private List<Hospital> allHospitals = new ArrayList<>();
    private List<Hospital> filteredHospitals = new ArrayList<>();

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_hospitals, container, false);
        hospitalsListView = view.findViewById(R.id.hospitals_list);
        searchInput = view.findViewById(R.id.search_input);
        progressBar = view.findViewById(R.id.progress_bar);
        hospitalAdapter = new HospitalAdapter(getContext(), filteredHospitals);
        hospitalsListView.setAdapter(hospitalAdapter);
        fetchHospitals();
        searchInput.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                filterHospitals(s.toString());
            }
            @Override
            public void afterTextChanged(Editable s) {}
        });
        return view;
    }

    private void fetchHospitals() {
        progressBar.setVisibility(View.VISIBLE);
        ApiService apiService = ApiClient.getClient().create(ApiService.class);
        apiService.getHospitals().enqueue(new Callback<List<Hospital>>() {
            @Override
            public void onResponse(Call<List<Hospital>> call, Response<List<Hospital>> response) {
                progressBar.setVisibility(View.GONE);
                if (response.isSuccessful() && response.body() != null) {
                    allHospitals.clear();
                    allHospitals.addAll(response.body());
                    filterHospitals(searchInput.getText().toString());
                } else {
                    Toast.makeText(getContext(), getString(R.string.app_error), Toast.LENGTH_SHORT).show();
                }
            }
            @Override
            public void onFailure(Call<List<Hospital>> call, Throwable t) {
                progressBar.setVisibility(View.GONE);
                Toast.makeText(getContext(), getString(R.string.app_error), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void filterHospitals(String query) {
        filteredHospitals.clear();
        for (Hospital h : allHospitals) {
            if (h.getName().toLowerCase().contains(query.toLowerCase())) {
                filteredHospitals.add(h);
            }
        }
        hospitalAdapter.notifyDataSetChanged();
    }
}
