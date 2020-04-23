package sample;

import javafx.collections.ListChangeListener;
import javafx.event.ActionEvent;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;

import java.io.IOException;

public class Send_controller extends Login_controller{

    public Label send_scene_username;
    public Label send_balance;
    public TextField receiver_address;
    public TextField amount;

    public void initialize() {
        send_scene_username.setText("Welcome " + Login_controller.username);
        API_operations.balance.addListener(new ListChangeListener<String>() {
            @Override
            public void onChanged(Change<? extends String> change) {
                send_balance.setText(API_operations.balance.get(0));
            }
        });
    }


    public void load_settings(ActionEvent actionEvent) throws IOException {
        Main.mainstage.setScene(Login_controller.settings_scene);
        Main.mainstage.show();
    }

    public void synchronize(ActionEvent actionEvent) throws IOException {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setContentText("Press okay to synchronize balance\nPlease wait until finished");
        alert.showAndWait();
        Settings_controller.api.get_balance();
    }

    public void reset(ActionEvent actionEvent) {
        reset_to_login_screen();
    }

    public void send(ActionEvent actionEvent) {
        if (amount.getText().equals("")){
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setContentText("Amount cannot be zero");
            alert.show();
        }
        Settings_controller.api.new_transaction(receiver_address.getText(), Float.parseFloat(amount.getText()));
    }
}
