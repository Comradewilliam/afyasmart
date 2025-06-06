package com.afyasmart;

import android.os.Bundle;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import com.afyasmart.model.ChatMessage;
import com.afyasmart.network.ApiClient;
import com.afyasmart.network.ApiService;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ChatFragment extends Fragment {
    private ListView chatListView;
    private EditText inputMessage;
    private Button sendButton;
    private ProgressBar progressBar;
    private ChatAdapter chatAdapter;
    private List<ChatMessage> chatMessages = new ArrayList<>();

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_chat, container, false);
        chatListView = view.findViewById(R.id.chat_list);
        inputMessage = view.findViewById(R.id.input_message);
        sendButton = view.findViewById(R.id.send_button);
        progressBar = view.findViewById(R.id.progress_bar);
        chatAdapter = new ChatAdapter(getContext(), chatMessages);
        chatListView.setAdapter(chatAdapter);

        sendButton.setOnClickListener(v -> sendMessage());
        return view;
    }

    private void sendMessage() {
        String message = inputMessage.getText().toString().trim();
        if (TextUtils.isEmpty(message)) return;
        chatMessages.add(new ChatMessage(message, true));
        chatAdapter.notifyDataSetChanged();
        inputMessage.setText("");
        progressBar.setVisibility(View.VISIBLE);

        ApiService apiService = ApiClient.getClient().create(ApiService.class);
        Map<String, String> body = new HashMap<>();
        body.put("message", message);
        apiService.sendMessage(body).enqueue(new Callback<Map<String, Object>>() {
            @Override
            public void onResponse(Call<Map<String, Object>> call, Response<Map<String, Object>> response) {
                progressBar.setVisibility(View.GONE);
                if (response.isSuccessful() && response.body() != null) {
                    String reply = response.body().get("reply").toString();
                    chatMessages.add(new ChatMessage(reply, false));
                    chatAdapter.notifyDataSetChanged();
                } else {
                    Toast.makeText(getContext(), getString(R.string.chat_error), Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<Map<String, Object>> call, Throwable t) {
                progressBar.setVisibility(View.GONE);
                Toast.makeText(getContext(), getString(R.string.chat_error), Toast.LENGTH_SHORT).show();
            }
        });
    }
}
