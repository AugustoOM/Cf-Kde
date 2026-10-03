// SPDX-License-Identifier: MIT
import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

Item {
    id: root
    width: 1280
    height: 720
    component GateButton: Button {
        implicitHeight: 40
        palette.buttonText: "#f7eef1"
        background: Rectangle {
            radius: 10
            color: parent.down ? "#a13c50" : parent.hovered ? "#914153" : "#d0362530"
            border.color: "#66d9a7b4"
        }
    }
    component GateCombo: ComboBox {
        implicitHeight: 40
        palette.text: "#f7eef1"
        palette.buttonText: "#f7eef1"
        palette.base: "#30232c"
        palette.window: "#30232c"
        palette.highlight: "#99394a"
        background: Rectangle { radius: 10; color: "#ce231b23"; border.color: "#66d9a7b4" }
    }
    property bool busy: false
    function login() {
        if (user.currentText.length && !busy) {
            busy = true;
            message.text = "";
            sddm.login(user.currentText, password.text, session.currentIndex);
        }
    }
    Image {
        anchors.fill: parent
        source: config.background
        fillMode: Image.PreserveAspectCrop
    }
    Rectangle { anchors.fill: parent; color: "#440b080e" }
    // Each greeter window contains its own centered form on its monitor.
    ColumnLayout {
        anchors.centerIn: parent
        width: Math.min(360, root.width - 48)
        spacing: 16
        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            width: 88; height: 88; radius: 44
            color: "#44221b24"
            border.color: "#66ffffff"
            // Neutral avatar drawn with simple shapes, with padding to avoid clipping.
            Rectangle {
                width: 24; height: 24; radius: 12
                anchors.horizontalCenter: parent.horizontalCenter
                y: 18; color: "#f0e8ec"
            }
            Rectangle {
                width: 46; height: 25; radius: 12
                anchors.horizontalCenter: parent.horizontalCenter
                y: 48; color: "#f0e8ec"
            }
        }
        GateCombo {
            id: user
            Layout.fillWidth: true
            model: userModel
            textRole: "name"
            currentIndex: userModel.lastIndex >= 0 ? userModel.lastIndex : 0
            editable: true
            enabled: !root.busy
            font.family: "Noto Sans"
            font.pixelSize: 18
            onAccepted: password.forceActiveFocus()
        }
        TextField {
            id: password
            Layout.fillWidth: true
            implicitHeight: 46
            placeholderText: "Contraseña"
            color: "#f7eef1"
            placeholderTextColor: "#c4b1ba"
            background: Rectangle {
                radius: 10; color: "#d0231b23"
                border.color: password.activeFocus ? "#d37a8e" : "#66d9a7b4"
                border.width: password.activeFocus ? 2 : 1
            }
            echoMode: TextInput.Password
            enabled: !root.busy
            focus: true
            font.family: "Noto Sans"
            font.pixelSize: 16
            onAccepted: root.login()
            Keys.onEscapePressed: { text = ""; message.text = ""; }
        }
        GateButton {
            Layout.fillWidth: true
            text: root.busy ? "Ingresando…" : "Iniciar sesión"
            enabled: !root.busy
            onClicked: root.login()
        }
        Label {
            id: message
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
            color: "#fff2f4"
            wrapMode: Text.WordWrap
        }
    }
    RowLayout {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 28
        width: Math.min(root.width - 48, 720)
        spacing: 12
        GateCombo {
            id: session
            Layout.fillWidth: true
            model: sessionModel
            textRole: "name"
            currentIndex: sessionModel.lastIndex
        }
        GateCombo {
            id: layout
            Layout.preferredWidth: 160
            model: keyboard.layouts
            textRole: "longName"
            displayText: count > 0 ? currentText : "Teclado actual"
            enabled: count > 1
            currentIndex: keyboard.currentLayout
            onActivated: keyboard.currentLayout = currentIndex
        }
        GateButton { text: "Reiniciar"; visible: sddm.canReboot; onClicked: sddm.reboot() }
        GateButton { text: "Apagar"; visible: sddm.canPowerOff; onClicked: sddm.powerOff() }
    }
    Connections {
        target: sddm
        function onLoginFailed() {
            root.busy = false;
            password.text = "";
            message.text = "No se pudo iniciar sesión. Revisá usuario y contraseña.";
            password.forceActiveFocus();
        }
        function onLoginSucceeded() { root.busy = true; }
    }
    Component.onCompleted: password.forceActiveFocus()
}
