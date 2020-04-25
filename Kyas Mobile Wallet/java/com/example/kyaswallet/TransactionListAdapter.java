package com.example.kyaswallet;

import android.annotation.SuppressLint;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.kyaswallet.R;
import com.example.kyaswallet.Transaction;

import java.text.DecimalFormat;
import java.util.Currency;
import java.util.List;

public class TransactionListAdapter extends RecyclerView.Adapter<TransactionListAdapter.TransactionViewHolder> {

    private final LayoutInflater inflater;
    private List<Transaction> transactions;

    TransactionListAdapter(Context context) {
        inflater = LayoutInflater.from(context);
    }

    @SuppressLint("SetTextI18n")
    //add UI elements to UI view holder
    public void onBindViewHolder(@NonNull TransactionViewHolder holder, int position) {
        Transaction currentTransaction = transactions.get(position);
        if (currentTransaction.getSender().equals(Address.getAddress())){
            holder.amountTv.setText(String.valueOf(-currentTransaction.getAmount()));
        }else{
            holder.amountTv.setText(String.valueOf(currentTransaction.getAmount()));
        }

        holder.recipientTv.setText("Recipient: " + currentTransaction.getRecipient());
        holder.senderTv.setText("Sender: " + currentTransaction.getSender());


    }

    @NonNull
    @Override
    // inflate transaction view and return finished Holder
    public TransactionViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View transactionView = inflater.inflate(R.layout.transaction_layout, parent, false);
        return new TransactionViewHolder(transactionView);
    }

    @Override
    //get amount of transactions
    public int getItemCount() {
        if (transactions != null) {
            return transactions.size();
        } else return 0;
    }

    // set transactions to provided List from back
    void setItems(List<Transaction> transactionList) {
        transactions = transactionList;
        notifyDataSetChanged();
    }

    //Holder subclass
    static class TransactionViewHolder extends RecyclerView.ViewHolder {
        private final TextView amountTv;
        private final TextView recipientTv;
        private final TextView senderTv;


        private TransactionViewHolder(@NonNull View itemView) {
            super(itemView);
            amountTv = itemView.findViewById(R.id.amount_textView);
            recipientTv = itemView.findViewById(R.id.recipient_textview);
            senderTv = itemView.findViewById(R.id.sender_textView);


        }
    }

}
