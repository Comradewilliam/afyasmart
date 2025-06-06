package com.afyasmart;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;
import com.afyasmart.model.ChatMessage;
import java.util.List;

public class ChatAdapter extends BaseAdapter {
    private Context context;
    private List<ChatMessage> messages;
    private static final int TYPE_USER = 0;
    private static final int TYPE_BOT = 1;

    public ChatAdapter(Context context, List<ChatMessage> messages) {
        this.context = context;
        this.messages = messages;
    }

    @Override
    public int getCount() {
        return messages.size();
    }

    @Override
    public Object getItem(int position) {
        return messages.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public int getItemViewType(int position) {
        return messages.get(position).isUser() ? TYPE_USER : TYPE_BOT;
    }

    @Override
    public int getViewTypeCount() {
        return 2;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        ChatMessage message = messages.get(position);
        int type = getItemViewType(position);
        if (convertView == null) {
            if (type == TYPE_USER) {
                convertView = LayoutInflater.from(context).inflate(R.layout.item_chat_user, parent, false);
            } else {
                convertView = LayoutInflater.from(context).inflate(R.layout.item_chat_bot, parent, false);
            }
        }
        TextView textView = convertView.findViewById(R.id.message_text);
        textView.setText(message.getMessage());
        return convertView;
    }
}
