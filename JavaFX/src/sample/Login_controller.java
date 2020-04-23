package sample;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;

import java.io.IOException;

public class Login_controller {

    public TextField login_screen_username;
    public static String username;
    public static Scene settings_scene, send_scene;


    public void reset_to_login_screen() {
        try {
            API_operations.balance.set(0, "0");
            Parent settings_changer = FXMLLoader.load(getClass().getResource("kyas_settings.fxml"));
            settings_scene = new Scene(settings_changer);
            Parent send_changer = FXMLLoader.load(getClass().getResource("kyas_send.fxml"));
            send_scene = new Scene(send_changer);
            Parent login_changer = FXMLLoader.load(getClass().getResource("kyas_login.fxml"));
            Scene login_scene = new Scene(login_changer);
            Main.mainstage.setScene(login_scene);
            Main.mainstage.show();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void login(ActionEvent actionEvent) throws IOException {
        username = login_screen_username.getText();
        try {
            Parent settings_changer = FXMLLoader.load(getClass().getResource("kyas_settings.fxml"));
            settings_scene = new Scene(settings_changer);
            Parent send_changer = FXMLLoader.load(getClass().getResource("kyas_send.fxml"));
            send_scene = new Scene(send_changer);
        } catch (IOException e) {
            e.printStackTrace();
        }
        Main.mainstage.setScene(settings_scene);
        Main.mainstage.show();
    }
}


