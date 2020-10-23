import QtQuick.Controls 2.10
import QtQuick.Layouts 1.10
import QtQuick 2.5

Rectangle {
    id: okaneApp

    RowLayout {
        id: toolboxRowLayout
        Button {
            text: "Accounts"
            //onClicked: model.submit()
        }
        Button {
            text: "Balance"
            //onClicked: model.revert()
        }
    }

    Rectangle {
        id: mainArea

        AccountsList {
            visible: false
        }

        BalanceList {
            visible: false
        }
    }
}