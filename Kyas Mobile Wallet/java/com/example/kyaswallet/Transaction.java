package com.example.kyaswallet;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

//Base Transaction class
public class Transaction {

    @SerializedName("betrag")
    @Expose
    private double amount;

    @SerializedName("empfänger")
    @Expose
    private String recipient;

    @SerializedName("absender")
    private String sender;

    public Transaction(double amount, String recipient, String sender) {
        this.amount = amount;
        this.recipient = recipient;
        this.sender = sender;
    }



    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public String getRecipient() {
        return recipient;
    }

    public void setRecipient(String recipient) {
        this.recipient = recipient;
    }

    public String getSender() {
        return sender;
    }

    public void setSender(String sender) {
        this.sender = sender;
    }
}
