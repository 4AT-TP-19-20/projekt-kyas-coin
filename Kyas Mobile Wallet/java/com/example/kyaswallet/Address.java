package com.example.kyaswallet;

public class Address {

    private static String address = "_/_";

    private static double balance = 0;

    public static double getBalance() {
        return balance;
    }

    public static void setBalance(double balance) {
        Address.balance = balance;
    }

    public static String getAddress() {
        return address;
    }

    public static void setAddress(String address) {
        Address.address = address;
    }
}