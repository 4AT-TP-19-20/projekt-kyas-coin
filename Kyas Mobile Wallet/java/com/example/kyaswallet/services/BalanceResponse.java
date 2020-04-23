package com.example.kyaswallet.services;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class BalanceResponse {

    @SerializedName("balance")
    @Expose
    private double balance;

    public double getBalance() {
        return balance;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }
}
