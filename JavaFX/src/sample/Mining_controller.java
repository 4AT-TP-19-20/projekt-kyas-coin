package sample;

import com.sun.scenario.Settings;
import javafx.collections.ListChangeListener;
import javafx.event.ActionEvent;
import javafx.scene.control.Alert;
import javafx.scene.control.Label;

import java.io.IOException;

public class Mining_controller extends Login_controller {

    public Label mining_scene_username;
    public Label mining_balance;

    public void initialize() {
        mining_scene_username.setText("Welcome " + Login_controller.username);
        API_operations.balance.addListener(new ListChangeListener<String>() {
            @Override
            public void onChanged(Change<? extends String> change) {
                mining_balance.setText(API_operations.balance.get(0));
            }
        });
    }

    public void synchronize(ActionEvent actionEvent) throws IOException {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setContentText("Balance synchronizing\nPlease wait until finished");
        alert.showAndWait();
        Settings_controller.api.get_balance();
        alert.setContentText("Balance synchronized");
        alert.show();
    }

    public void reset(ActionEvent actionEvent) {
        reset_to_login_screen();
    }

    public void start_mining(ActionEvent actionEvent) {
        Settings_controller.api.mining();
    }

    public void load_send(ActionEvent actionEvent) {
        Main.mainstage.setScene(Login_controller.send_scene);
        Main.mainstage.show();
    }

    public void load_settings(ActionEvent actionEvent) {
        Main.mainstage.setScene(Login_controller.settings_scene);
        Main.mainstage.show();
    }
}
