package com.example.kyaswallet;

import android.os.Build;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import java.lang.annotation.AnnotationFormatError;

public class SettingsActivity extends AppCompatActivity {

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        TextView currentAddrTv = findViewById(R.id.currentAddressTv);
        final EditText newAddrEt = findViewById(R.id.newAddressEt);
        if (!Address.getAddress().equals("_/_"))
            currentAddrTv.setText(Address.getAddress());

        ImageView saveBtn = findViewById(R.id.save_settings_button);
        saveBtn.setImageDrawable(getDrawable(R.drawable.ic_check_white_24dp));
        saveBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Empty amount, set "CANCEL" reply
                if (TextUtils.isEmpty(newAddrEt.getText())) {
                    setResult(RESULT_CANCELED);
                }
                // Add data to db directly over ViewModel
                else {
                    Address.setAddress(newAddrEt.getText().toString());
                    setResult(RESULT_OK);
                }
                finish();
            }
        });



    }
}
