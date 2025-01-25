import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 600
    height: 400
    title: "srtd"

    Rectangle {
        width: parent.width / 2
        height: parent.height
        color: "#F2DFB7"

        Column {
            anchors.fill: parent
            spacing: 10 // Add spacing between header and scroll view

            // Header area with "Files" text
            Rectangle {
                width: parent.width
                height: 40
                color: "#E0E0E0"

                Text {
                    text: "Files"
                    font.bold: true
                    anchors.centerIn: parent
                }
            }

            // Scrollable content below the header
            ScrollView {
                width: parent.width
                height: parent.height - 40 - 10  // Subtract header and spacing height
                // style: ScrollViewStyle {
                //     ScrollBar.vertical: ScrollBar {
                //         width: 12
                //         background: Rectangle {
                //             color: "transparent"
                //             radius: 6
                //         }
                //         handle: Rectangle {
                //             width: 12
                //             height: 50
                //             color: "#C0E0E0"
                //             radius: 6
                //         }
                //     }
                // }
                Column {
                    id: column
                    spacing: 5
                    width: parent.width
                    anchors.left: parent.left
                    anchors.top: parent.top

                    Repeater {
                        model: ListModel {
                            // List of files found in the source directory
                            ListElement { name: "schedule_955.xlsx" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "schedule_955.xlsx" }
                            ListElement { name: "schedule_955.xlsx" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "schedule_955.xlsx" }
                            ListElement { name: "schedule_955.xlsx" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "schedule_955.xlsx" }
                            ListElement { name: "schedule_955.xlsx" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "schedule_955.xlsx" }
                            ListElement { name: "schedule_955.xlsx" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "schedule_955.xlsx" }
                            ListElement { name: "schedule_955.xlsx" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "homework_606.txt" }
                            ListElement { name: "schedule_955.xlsx" }
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
    }
}
