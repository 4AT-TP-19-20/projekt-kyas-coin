package sample;

import javafx.event.ActionEvent;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Label;

import java.io.IOException;

public class Send_controller {

    public Label send_scene_username;

    public void initialize() {
        send_scene_username.setText(Login_controller.username);
    }

    public void load_settings(ActionEvent actionEvent) throws IOException {
        Main.mainstage.setScene(Login_controller.settings_scene);
        Main.mainstage.show();
    }

    public void synchronize(ActionEvent actionEvent) throws IOException {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setContentText("Press okay to synchronize blockchain\nPlease wait until finished");
        alert.showAndWait();
        Settings_controller.api.get_full_update();
    }
}
