package com.example.kyaswallet.services;

import com.example.kyaswallet.Transaction;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class TransactionsResponse {

    @SerializedName("transactions")
    @Expose
    private List<Transaction> transactionsList;

    public List<Transaction> getTransactionsList() {
        return transactionsList;
    }

    public void setTransactionsList(List<Transaction> transactionsList) {
        this.transactionsList = transactionsList;
    }
}
