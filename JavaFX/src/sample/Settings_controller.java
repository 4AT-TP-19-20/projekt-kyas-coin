package sample;

import javafx.event.ActionEvent;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;

import java.io.IOException;

public class Settings_controller {

    public Label settings_scene_username;
    public ComboBox<String> combobox_serverlist;
    public static String selected_masternode;
    public static API_operations api;
    public boolean first_time = true;

    public void initialize() {
        settings_scene_username.setText(Login_controller.username);
        api = new API_operations();
        combobox_serverlist.getItems().addAll(api.masternodes);
    }

    public void load_send(ActionEvent actionEvent) throws IOException, InterruptedException {
        selected_masternode = combobox_serverlist.getValue();
        if (selected_masternode == null) {
            Alert alert = new Alert(Alert.AlertType.WARNING);
            alert.setContentText("Please choose a masternode to sync from.");
            alert.show();
            return;
        }
        if (first_time) {
            api.set_masternode();
            Alert alert = new Alert(Alert.AlertType.INFORMATION);
            alert.setContentText("Press okay to synchronize blockchain\nPlease wait until finished");
            alert.showAndWait();
            api.register_user();
            api.get_full_update();
            first_time = false;
        }
        Main.mainstage.setScene(Login_controller.send_scene);
        Main.mainstage.show();
    }

    public void synchronize(ActionEvent actionEvent) throws IOException {
        if (first_time) {
            api.set_masternode();
            Alert alert = new Alert(Alert.AlertType.INFORMATION);
            alert.setContentText("Press okay to synchronize blockchain\nPlease wait until finished");
            alert.showAndWait();
            api.register_user();
            api.get_full_update();
            first_time = false;
        }
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setContentText("Press okay to synchronize blockchain\nPlease wait until finished");
        alert.showAndWait();
        api.get_full_update();
    }
}
