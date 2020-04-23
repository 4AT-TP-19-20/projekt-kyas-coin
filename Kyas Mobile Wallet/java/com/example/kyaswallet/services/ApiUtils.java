package com.example.kyaswallet.services;

import android.annotation.SuppressLint;
import android.util.Log;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

import com.example.kyaswallet.Address;
import com.example.kyaswallet.NewTransactionActivity;
import com.example.kyaswallet.Transaction;

import org.jetbrains.annotations.Nullable;

import java.io.IOException;
import java.util.List;


import io.reactivex.Scheduler;
import io.reactivex.Single;
import io.reactivex.SingleObserver;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.Disposable;
import io.reactivex.internal.schedulers.NewThreadScheduler;
import io.reactivex.schedulers.Schedulers;
import okhttp3.MediaType;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import okio.BufferedSink;
import retrofit2.Response;

public class ApiUtils {
    private static String BASE_URL = "http://173.212.211.222:2169";

    private static MutableLiveData<Double> BALANCE = new MutableLiveData<>();
    private static MutableLiveData<Integer> POST_RESPONSE_CODE = new MutableLiveData<>();
    private static MutableLiveData<List<Transaction>> TRANSACTIONS = new MutableLiveData<>();
    private static MutableLiveData<Integer> REGISTER_RESPONSE_CODE = new MutableLiveData<>();




    public static KyasService getKyasService(){
        return KyasClient.getKyasRetrofit(BASE_URL).create(KyasService.class);
    }




    @SuppressLint("CheckResult")
    public LiveData<Integer> postTransaction(double amount, String recipient, String sender){

        String body = "{" +
                "\"absender\":" + "\"" + sender + "\"" +
                ",\"empfänger\":" + "\"" + recipient + "\"" +
                ",\"betrag\":" +  amount +
                "}";

        RequestBody requestBody = RequestBody.create(MediaType.parse(body), body);

        final Single<Response<ResponseBody>> createKyas = getKyasService().createTransaction(requestBody);
        createKyas.subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new SingleObserver<Response<ResponseBody>>() {
                    @Override
                    public void onSubscribe(Disposable d) {
                        Log.d("API", "Connected to Kyas Tx Service");
                    }

                    @Override
                    public void onSuccess(Response<ResponseBody> response) {
                        POST_RESPONSE_CODE.setValue(response.code());
                    }

                    @Override
                    public void onError(Throwable e) {

                    }
                });

        return POST_RESPONSE_CODE;
    }

    public LiveData<Integer> registerAddress(){
        String address = Address.getAddress();
        String body = "{ \"name\": \"" + address + "\"}";

        RequestBody requestBody = RequestBody.create(MediaType.parse(body), body);

        final Single<Response<ResponseBody>> createKyas = getKyasService().registerAddress(requestBody);
        createKyas.subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new SingleObserver<Response<ResponseBody>>() {
                    @Override
                    public void onSubscribe(Disposable d) {
                        Log.d("API", "Connected to Kyas Registration Service");
                    }

                    @Override
                    public void onSuccess(Response<ResponseBody> response) {
                        REGISTER_RESPONSE_CODE.setValue(response.code());

                    }
                    @Override
                    public void onError(Throwable e) {

                    }
                });

        return POST_RESPONSE_CODE;
    }


    public LiveData<List<Transaction>> getTransactions(){
        String address = Address.getAddress();
        String body = "{ \"name\": \"" + address + "\"}";
        final RequestBody requestBody = RequestBody.create(MediaType.parse(body), body);
        final Single<Response<TransactionsResponse>> transactionsKyas = getKyasService().getTransactions(requestBody);
        transactionsKyas.subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new SingleObserver<Response<TransactionsResponse>>() {
                    @Override
                    public void onSubscribe(Disposable d) {
                        Log.d("API", "Connected to Kyas Tx Service");

                    }

                    @Override
                    public void onSuccess(Response<TransactionsResponse> transactionsResponseResponse) {
                        assert transactionsResponseResponse.body() != null;
                        TRANSACTIONS.setValue(transactionsResponseResponse.body().getTransactionsList());
                    }

                    @Override
                    public void onError(Throwable e) {

                    }
                });
        return TRANSACTIONS;
    }




    public LiveData<Double> getBalance(){
        String address = Address.getAddress();

        String body = "{ \"name\": \"" + address + "\"}";
        final RequestBody requestBody = RequestBody.create(MediaType.parse(body), body);

        final Single<Response<BalanceResponse>> balKyas = getKyasService().getBalance(requestBody);
        balKyas.subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new SingleObserver<Response<BalanceResponse>>() {
                    @Override
                    public void onSubscribe(Disposable d) {
                        Log.d("API", "Connected to Kyas Balance Service");
                    }

                    @Override
                    public void onSuccess(Response<BalanceResponse> balanceResponseResponse) {
                        assert balanceResponseResponse.body() != null;
                        Address.setBalance(balanceResponseResponse.body().getBalance());
                        BALANCE.setValue(balanceResponseResponse.body().getBalance());
                    }

                    @Override
                    public void onError(Throwable e) {

                    }
                });
        return BALANCE;
    }






}

