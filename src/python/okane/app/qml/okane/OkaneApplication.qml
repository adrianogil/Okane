import QtQuick.Controls 2.10
import QtQuick.Layouts 1.10
import QtQuick 2.5

Rectangle {
    id: okaneApp

    function showScreen(targetScreen) {
        accountsList.visible = false
        balanceList.visible = false

        targetScreen.visible = true
    }

    RowLayout {
        id: toolboxRowLayout

        anchors {
            top: okaneApp.top
            topMargin: 10
            left: okaneApp.left
            leftMargin: 10
        }

        Button {
            text: "Accounts"
            onClicked: showScreen(accountsList)
        }
        Button {
            text: "Balance"
            onClicked: showScreen(balanceList)
        }
    }

    Rectangle {
        id: mainArea

        x: 0.05 * okaneApp.width
        width: 0.9 * okaneApp.width
        height: okaneApp.height - 100

        anchors {
            top: toolboxRowLayout.bottom
            topMargin: 20
        }

        AccountsList {
            id: accountsList
            visible: false

            anchors.fill: parent
        }

        BalanceList {
            id: balanceList
            visible: false

            anchors.fill: parent   
        }
    }
}