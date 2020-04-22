package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class Main extends Application {
    public static Stage mainstage;
    @Override
    public void start(Stage primaryStage) throws Exception {
        Parent root = FXMLLoader.load(getClass().getResource("kyas_login.fxml"));
        mainstage = primaryStage;
        mainstage.setTitle("");
        mainstage.setScene(new Scene(root));
        mainstage.show();
    }


    public static void main(String[] args) {
        launch(args);
    }
}
