package com.example.kyaswallet;

import android.os.Build;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;

import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProviders;

//Send transaction screem
public class NewTransactionActivity extends AppCompatActivity {

    private EditText amountEt;
    private EditText recipientEt;

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_add_transaction);

        //Initialise Textboxes
        amountEt = findViewById(R.id.amountTf);
        recipientEt = findViewById(R.id.recipientTf);

        //Initialise save button
        ImageView saveBtn = findViewById(R.id.save_button);
        saveBtn.setImageDrawable(getDrawable(R.drawable.ic_check_white_24dp));
        saveBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                TransactionViewModel transactionViewModel = ViewModelProviders.of(NewTransactionActivity.this).get(TransactionViewModel.class);
                // Empty amount, set "CANCEL" reply
                if (TextUtils.isEmpty(amountEt.getText())) {
                    setResult(RESULT_CANCELED);
                }
                // Create and add new Transaction to viewmodel
                else {
                    double amount = Double.parseDouble(amountEt.getText().toString());
                    String recipient = recipientEt.getText().toString();
                    Transaction newTransaction = new Transaction(amount, recipient, Address.getAddress());
                    transactionViewModel.create(newTransaction);
                    setResult(RESULT_OK);
                }
                finish();
            }
        });





    }
}
