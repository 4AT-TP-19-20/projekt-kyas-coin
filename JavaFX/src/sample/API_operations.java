package sample;

import javafx.scene.control.Alert;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;


import java.nio.charset.StandardCharsets;
import java.util.ArrayList;


public class API_operations {
    public ArrayList<String> masternodes = new ArrayList<>();
    public ArrayList<String> masternode_urls = new ArrayList<>();

    API_operations() {
        masternodes.add("vmi332355.contaboserver.net");
        masternode_urls.add("http://173.212.211.222:2169");
    }


    void register_user() {
        try {
            URL url = new URL("http://localhost:2169/set/name");
            var parameters = "{\"name\": \"" + Login_controller.username + "\"}";
            byte[] postData = parameters.getBytes(StandardCharsets.UTF_8);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("User-Agent", "Java client");
            connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            var writer = new DataOutputStream(connection.getOutputStream());
            writer.write(postData);
            StringBuilder content;

            try (var br = new BufferedReader(
                    new InputStreamReader(connection.getInputStream()))) {

                String line;
                content = new StringBuilder();

                while ((line = br.readLine()) != null) {
                    content.append(line);
                    content.append(System.lineSeparator());
                }
            }
            connection.disconnect();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }


    void get_full_update() throws IOException {

        try {
            URL url = new URL("http://localhost:2169/get/full/update");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            StringBuilder content;
            try (var br = new BufferedReader(
                    new InputStreamReader(connection.getInputStream()))) {
                String line;
                content = new StringBuilder();

                while ((line = br.readLine()) != null) {
                    content.append(line);
                    content.append(System.lineSeparator());
                }
            }
            connection.disconnect();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    void set_masternode() {
        if (Settings_controller.selected_masternode.equals(masternodes.get(0))) {

            try {
                URL url = new URL("http://localhost:2169/set/masternode");
                var parameters = "{\"masternode\": \"http://173.212.211.222:2169\"}";
                byte[] postData = parameters.getBytes(StandardCharsets.UTF_8);
                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                connection.setDoOutput(true);
                connection.setRequestMethod("POST");
                connection.setRequestProperty("User-Agent", "Java client");
                connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
                var writer = new DataOutputStream(connection.getOutputStream());
                writer.write(postData);
                StringBuilder content;

                try (var br = new BufferedReader(
                        new InputStreamReader(connection.getInputStream()))) {

                    String line;
                    content = new StringBuilder();

                    while ((line = br.readLine()) != null) {
                        content.append(line);
                        content.append(System.lineSeparator());
                    }
                }
                connection.disconnect();
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }


        }
    }

}
