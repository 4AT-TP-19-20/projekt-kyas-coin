package sample;

import javafx.collections.ListChangeListener;
import javafx.event.ActionEvent;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;

import javax.swing.event.ChangeListener;
import java.io.IOException;

public class Settings_controller extends Login_controller {

    public Label settings_scene_username;
    public ComboBox<String> combobox_serverlist;
    public static String selected_masternode;
    public static API_operations api;
    public boolean first_time = true;
    public Label settings_balance;


    public void initialize() {
        settings_scene_username.setText(Login_controller.username);
        api = new API_operations();
        combobox_serverlist.getItems().addAll(api.masternodes);
        API_operations.balance.add("0");
        settings_balance.setText(API_operations.balance.get(0));
        API_operations.balance.addListener(new ListChangeListener<String>() {
            @Override
            public void onChanged(Change<? extends String> change) {
                settings_balance.setText(API_operations.balance.get(0));
            }
        });
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
            alert.setContentText("Press okay to synchronize balance\nPlease wait until finished");
            alert.showAndWait();
            api.register_user();
            api.get_balance();
            first_time = false;
        }

        Main.mainstage.setScene(Login_controller.send_scene);
        Main.mainstage.show();
    }

    public void synchronize(ActionEvent actionEvent) throws IOException {
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
            api.get_balance();
            first_time = false;
            return;
        }
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setContentText("Press okay to synchronize blockchain\nPlease wait until finished");
        alert.showAndWait();
        Settings_controller.api.get_balance();
    }

    public void reset(ActionEvent actionEvent) {
        reset_to_login_screen();
    }
}
