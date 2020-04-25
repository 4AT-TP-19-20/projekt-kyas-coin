package com.example.kyaswallet.services;

import retrofit2.Retrofit;
import retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory;
import retrofit2.converter.gson.GsonConverterFactory;

public class KyasClient {
    private static Retrofit KyasRetrofit = null;

    //Retrofit Client
    public static Retrofit getKyasRetrofit(String baseURL) {
        if (KyasRetrofit == null) {
            KyasRetrofit = new Retrofit.Builder()
                    .baseUrl(baseURL)
                    .addConverterFactory(GsonConverterFactory.create())
                    .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
                    .build();
        }
        return KyasRetrofit;
    }

}
