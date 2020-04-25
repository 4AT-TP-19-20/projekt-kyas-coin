package com.example.kyaswallet;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

//Base Transaction class
public class Transaction {

    @SerializedName("amount")
    @Expose
    private double amount;

    @SerializedName("recipient")
    @Expose
    private String recipient;

    @SerializedName("sender")
    private String sender;

    @SerializedName("index_block")
    private int block;

    public Transaction(double amount, String recipient, String sender) {
        this.amount = amount;
        this.recipient = recipient;
        this.sender = sender;
    }

    public Transaction(double amount, String recipient, String sender, int block) {
        this.amount = amount;
        this.recipient = recipient;
        this.sender = sender;
        this.block = block;
    }

    public int getBlock() {
        return block;
    }

    public void setBlock(int block) {
        this.block = block;
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
