import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 600
    height: 400
    title: "srtd"

    Rectangle {
        width: 300
        height: 400
        color: "#E0E0E0"

        Column {
            spacing: 5
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 10
            anchors.topMargin: 10

            Text {
                text: "Files"
                font.bold: true
            }

            Repeater {
                model: ListModel {
                    ListElement { name: "schedule_955.xlsx" }
                    ListElement { name: "homework_606.txt" }
                    ListElement { name: "homework_606.txt" }
                    ListElement { name: "schedule_955.xlsx" }
                    // Add more file names as needed
                }

                delegate: Row {
                    spacing: 5
                    Rectangle {
                        width: 10
                        height: 10
                        color: "black"
                    }
                    Text {
                        text: model.name
                    }
                }
            }
        }
    }

    Rectangle {
        width: 150
        height: 200
        color: "#C0E0E0"
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 10
        anchors.topMargin: 10
    }

    Column {
        spacing: 5
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.leftMargin: 10
        anchors.bottomMargin: 10

        Repeater {
            model: ListModel {
                ListElement { name: "schedule_955.xlsx" }
                ListElement { name: "homework_606.txt" }
                ListElement { name: "notes_902.json" }
                // Add more file names as needed
            }

            delegate: Row {
                spacing: 5
                Rectangle {
                    width: 10
                    height: 10
                    color: "black"
                }
                Text {
                    text: model.name
                }
            }
        }
    }
}
