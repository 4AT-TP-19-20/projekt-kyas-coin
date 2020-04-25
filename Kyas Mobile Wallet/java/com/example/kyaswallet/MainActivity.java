package com.example.kyaswallet;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import java.text.DecimalFormat;
import java.util.Arrays;
import java.util.List;

//Main screen
public class MainActivity extends AppCompatActivity {

    private static final int NEW_TX_REQUEST_CODE = 1;
    private static final int SETTINGS_REQUEST_CODE = 1;


    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Init ViewModel
        final TransactionViewModel transactionViewModel = ViewModelProviders.of(this)
                .get(TransactionViewModel.class);

        //RecyclerView setup
        RecyclerView recyclerView = findViewById(R.id.recyclerview);
        final TransactionListAdapter adapter = new TransactionListAdapter(this);
        recyclerView.setAdapter(adapter);
        LinearLayoutManager l = new LinearLayoutManager(this);
        recyclerView.setLayoutManager(l);

        //Toolbar Button setup
        ImageView addIb = findViewById(R.id.add_expense_button_main);
        addIb.setImageDrawable(getDrawable(R.drawable.ic_add_white_24dp));
        addIb.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, NewTransactionActivity.class);
                startActivityForResult(intent, NEW_TX_REQUEST_CODE);
            }
        });

        ImageView settingsIb = findViewById(R.id.settings_button_main);
        settingsIb.setImageDrawable(getDrawable(R.drawable.ic_settings_white_24dp));
        settingsIb.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent settingsIntent = new Intent(MainActivity.this, SettingsActivity.class);
                startActivityForResult(settingsIntent, SETTINGS_REQUEST_CODE);
            }
        });
        final double[] balance = {0};
        final TextView balanceTv = findViewById(R.id.balanceTv);
        ImageView refreshIb = findViewById(R.id.refresh_button_main);
        refreshIb.setImageDrawable(getDrawable(R.drawable.ic_refresh_white_24dp));
        refreshIb.setOnClickListener(new View.OnClickListener() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onClick(View v) {
                transactionViewModel.getBalance();
                DecimalFormat df2 = new DecimalFormat("0.00");
                String balString = df2.format(balance[0]).toString();
                balanceTv.setText(balString + " K");
                transactionViewModel.getAllTransactions();
            }
        });



        //Data Observers
        LiveData<Double> liveBalance = transactionViewModel.getBalance();
        liveBalance.observeForever(new Observer<Double>() {
            @Override
            public void onChanged(Double aDouble) {
                balance[0] = aDouble;
            }
        });


        transactionViewModel.getAllTransactions().observe(this, new Observer<List<Transaction>>() {
            @Override
            public void onChanged(List<Transaction> expenses) {
                adapter.setItems(expenses);
            }
        });





    }
}
