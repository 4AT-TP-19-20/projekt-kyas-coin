package com.example.kyaswallet;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.Observer;

import com.example.kyaswallet.services.ApiUtils;

import java.util.List;

//Frontends inner workings
public class TransactionViewModel extends AndroidViewModel {

    private final MutableLiveData<List<Transaction>> allExpenses = new MutableLiveData<>();
    private MutableLiveData<Double> BALANCE = new MutableLiveData<>();


    public TransactionViewModel(Application application) {
        super(application);
    }

    public LiveData<List<Transaction>> getAllTransactions(){
        ApiUtils utils = new ApiUtils();
        LiveData<List<Transaction>> liveTransactions = utils.getTransactions();
        liveTransactions.observeForever(new Observer<List<Transaction>>() {
            @Override
            public void onChanged(List<Transaction> transactions) {
                allExpenses.setValue(transactions);
            }
        });
        return allExpenses;
    }


    LiveData<Double> getBalance(){
        ApiUtils utils = new ApiUtils();
        utils.registerAddress();
        LiveData<Double> liveBalance = utils.getBalance();
        liveBalance.observeForever(new Observer<Double>() {
            @Override
            public void onChanged(Double aDouble) {
                BALANCE.setValue(aDouble);
            }
        });
        return BALANCE;
    }


    public void create(final Transaction transaction){
        ApiUtils utils = new ApiUtils();
        LiveData<Integer> createCode = utils.postTransaction(transaction.getAmount(), transaction.getRecipient(), transaction.getSender());
        createCode.observeForever(new Observer<Integer>() {
            @Override
            public void onChanged(Integer integer) {
                if (integer != 201)
                    throw new RuntimeException("No internet connection!");

            }
        });

    }

}
