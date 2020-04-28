package sample;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.control.Alert;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;


import java.nio.charset.StandardCharsets;
import java.util.ArrayList;


public class API_operations {
    public ArrayList<String> masternodes = new ArrayList<>();
    public ArrayList<String> masternode_urls = new ArrayList<>();
    public static ObservableList<String> balance = FXCollections.observableArrayList();

    API_operations() {
        masternodes.add("vmi332355.contaboserver.net");
        masternode_urls.add("http://173.212.211.222:2169");
    }


    public void register_user() {
        try {
            URL url = new URL("http://localhost:2169/set/name");
            var parameters = "{\"name\": \"" + Login_controller.username + "\"}";
            byte[] postData = parameters.getBytes(StandardCharsets.UTF_8);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("User-Agent", "Java client");
            connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            connection.setConnectTimeout(120000);
            connection.setReadTimeout(120000);
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
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setContentText("No response from local node\nQuitting...");
            alert.showAndWait();
            System.exit(1);
        } catch (IOException e) {
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setContentText("No response from local node\nQuitting...");
            alert.showAndWait();
            System.exit(1);
        }

    }


    public void get_balance() throws IOException {
        try {
            URL url = new URL("http://localhost:2169/specific/balance");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(120000);
            connection.setReadTimeout(120000);
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
            String n = "KYS ";
            balance.set(0, n.concat(content.toString()));
            connection.disconnect();
        } catch (MalformedURLException e) {
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setContentText("No response from local node\nQuitting...");
            alert.showAndWait();
            System.exit(1);
        } catch (IOException e) {
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setContentText("No response from local node\nQuitting...");
            alert.showAndWait();
            System.exit(1);
        }

    }

    public void set_masternode() {
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
                connection.setConnectTimeout(120000);
                connection.setReadTimeout(120000);
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
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setContentText("No response from local node\nQuitting...");
                alert.showAndWait();
                System.exit(1);
            } catch (IOException e) {
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setContentText("No response from local node\nQuitting...");
                alert.showAndWait();
                System.exit(1);
            }
        }
    }

    public void new_transaction(String empfänger, float betrag) {
        try {
            URL url = new URL("http://localhost:2169/transactions/new");
            var parameters = "{\"recipient\": \"" + empfänger + "\", \"amount\": " + betrag + "}";
            byte[] postData = parameters.getBytes(StandardCharsets.UTF_8);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("User-Agent", "Java client");
            connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            connection.setConnectTimeout(120000);
            connection.setReadTimeout(120000);

            var writer = new DataOutputStream(connection.getOutputStream());
            writer.write(postData);
            StringBuilder content;
            if (connection.getResponseCode() == 403) {
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setContentText("Balance not sufficient. Updating balance.");
                alert.show();
                get_balance();
            }
            if (connection.getResponseCode() == 201) {
                Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
                alert.setContentText("Transaction successful. Updating balance.");
                alert.show();
                get_balance();
                try (var br = new BufferedReader(
                        new InputStreamReader(connection.getInputStream()))) {

                    String line;
                    content = new StringBuilder();

                    while ((line = br.readLine()) != null) {
                        content.append(line);
                        content.append(System.lineSeparator());
                    }
                }
            }
            connection.disconnect();
        } catch (MalformedURLException e) {
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setContentText("No response from local node\nQuitting...");
            alert.showAndWait();
            System.exit(1);
        } catch (IOException e) {
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setContentText("No response from local node\nQuitting...");
            alert.showAndWait();
            System.exit(1);
        }
    }

    public void mining() {
        try {
            URL url = new URL("http://localhost:2169/mine");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(120000);
            connection.setReadTimeout(120000);
            if (connection.getResponseCode() == 200) {
                Alert alert = new Alert(Alert.AlertType.INFORMATION);
                alert.setContentText("Block has been successfully mined.\nReward will be added to the next block.");
                alert.show();
            } else if (connection.getResponseCode() == 403) {
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setContentText("PoW has already been calculated by someone else!\nPlease wait until next block.");
                alert.show();
            }
            connection.disconnect();
        } catch (MalformedURLException e) {
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setContentText("No response from local node\nQuitting...");
            alert.showAndWait();
            System.exit(1);
        } catch (IOException e) {
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setContentText("No response from local node\nQuitting...");
            alert.showAndWait();
            System.exit(1);
        }

    }
}


