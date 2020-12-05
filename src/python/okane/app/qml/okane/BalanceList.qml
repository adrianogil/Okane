import QtQuick.Controls 2.10
import QtQuick.Layouts 1.10
import QtQuick 2.5

Rectangle {
    id: screen
    
    border {
        width: 1
        color: "black"
    }
    radius: 10

    Text {
        text: "Balance"
        font.pixelSize: 20

        anchors {
            top: screen.top
            topMargin: 15
            horizontalCenter: screen.horizontalCenter
        }
    }

}