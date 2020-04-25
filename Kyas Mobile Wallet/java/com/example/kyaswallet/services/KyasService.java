package com.example.kyaswallet.services;


import org.intellij.lang.annotations.JdkConstants;

import java.net.ResponseCache;

import io.reactivex.Single;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Response;
import retrofit2.http.Body;
import retrofit2.http.POST;

//Retrofit API interface
public interface KyasService {

    @POST("/transactions/new")
    Single<Response<ResponseBody>> createTransaction (@Body RequestBody body);

    @POST("/client/balance")
    Single<Response<BalanceResponse>> getBalance (@Body RequestBody body);

    @POST("/client/transactions")
    Single<Response<TransactionsResponse>> getTransactions (@Body RequestBody body);

    @POST("/register")
    Single<Response<ResponseBody>> registerAddress (@Body RequestBody body);

}
