import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QAction, QHeaderView, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QInputDialog
import matplotlib.pyplot as plt
import seaborn as sns


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the title and size of the main window
        self.setWindowTitle("Predict Laptop Price")
        self.resize(800, 600)

        # Create a layout for the main window
        layout = QVBoxLayout()

        # Create a table widget to display the CSV data
        self.table_widget = QTableWidget()
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.verticalHeader().setVisible(False)

        # Add the table widget to the layout
        layout.addWidget(self.table_widget)

        # Create a widget to hold the search controls
        search_widget = QWidget()
        search_layout = QHBoxLayout()

        # Add a label and a line edit for the search text
        search_label = QLabel("Search:")
        self.search_line_edit = QLineEdit()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_line_edit)

        # Add a combobox to select the category for searching
        self.category_combobox = QComboBox()
        self.category_combobox.addItem("All")
        self.category_combobox.addItem("Company")
        self.category_combobox.addItem("Ram")
        self.category_combobox.addItem("Price")
        search_layout.addWidget(self.category_combobox)

        # Add a search button and a clear button
        search_button = QPushButton("Search")
        clear_button = QPushButton("Clear")
        search_button.clicked.connect(self.search_data)
        clear_button.clicked.connect(self.clear_search)
        search_layout.addWidget(search_button)
        search_layout.addWidget(clear_button)

        # Add the search controls to the search widget
        search_widget.setLayout(search_layout)

        # Add the search widget to the layout
        layout.addWidget(search_widget)

        # Create a widget to hold the add, delete, edit and save controls
        edit_widget = QWidget()
        edit_layout = QHBoxLayout()

        # Add a button to add a new row
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_new_data)
        edit_layout.addWidget(add_button)
        
        # Add a button to add a new row
        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(self.plot_Price)
        edit_layout.addWidget(plot_button)
        
        # predict_button = QPushButton("Predict")
        # predict_button.clicked.connect(self.predict_Price)
        # edit_layout.addWidget(predict_button)

        # Add a button to delete the selected row
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_row)
        edit_layout.addWidget(delete_button)

        # Add a button to edit the selected row
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.update_new_data)
        edit_layout.addWidget(edit_button)

        # Add a button to save the changes to the CSV file
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_changes)
        edit_layout.addWidget(save_button)

        # Add the edit controls to the edit widget
        edit_widget.setLayout(edit_layout)

        # Add the edit widget to the layout
        layout.addWidget(edit_widget)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget for the main window
        self.setCentralWidget(central_widget)

        # Load the CSV data into a pandas DataFrame
        self.data = pd.read_csv("laptop_data.csv")

        # Populate the table widget with the CSV data
        self.populate_table_widget()
        # self.update_new_data()

    def populate_table_widget(self):
    # Set the number of rows and columns in the table widget
        num_rows, num_cols = self.data.shape
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(num_cols)

        # Set the horizontal headers for the table widget
        self.table_widget.setHorizontalHeaderLabels(self.data.columns)

        # Loop through the rows and columns of the data and populate the table widget
        for row in range(num_rows):
            for col in range(num_cols):
                item = QTableWidgetItem(str(self.data.iloc[row, col]))
                self.table_widget.setItem(row, col, item)

    def plot_Price(self):
        sns.barplot(x=self.data['TypeName'],y=self.data['Price'])
        plt.xticks(rotation='vertical')
        plt.show()
        
    def predict_Price(self):
        pass
        # self.predictor = laptop.LaptopPricePredictor()
        # self.predictor.show()
        

    def add_new_data(self):
        num_cols = self.table_widget.columnCount()
        row_data = []
        for i in range(num_cols):
            data, ok = QInputDialog.getText(self, f"Enter data for column {self.data.columns[i]}", f"Data for {self.data.columns[i]}")
            if ok:
                row_data.append(data)
            else:
                return

        # Add the new row to the DataFrame
        new_row = pd.Series(row_data, index=self.data.columns)
        self.data = self.data.append(new_row, ignore_index=True)
        num_rows = self.table_widget.rowCount()
        self.table_widget.insertRow(num_rows)
        for i, data in enumerate(row_data):
            self.table_widget.setItem(num_rows, i, QTableWidgetItem(data))


    def delete_row(self):
        # Delete the selected row from the table widget and the data
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            self.table_widget.removeRow(selected_row)
            self.data.drop(selected_row, inplace=True)
            self.data.reset_index(drop=True, inplace=True)

    def update_new_data(self):
        num_cols = self.table_widget.columnCount()
        selected_row = self.table_widget.currentRow()

        # If no row is selected, return without updating
        if selected_row < 0:
            return

        row_data = []
        for i in range(num_cols):
            data = str(self.data.iloc[selected_row][i])
            data, ok = QInputDialog.getText(self, f"Enter data for column {self.data.columns[i]}", f"Data for {self.data.columns[i]}", text=str(self.data.iloc[selected_row][i]))
            if ok:
                row_data.append(data)
            else:
                return

        # Replace the existing row with the new data
        self.data.iloc[selected_row] = row_data
        for i, data in enumerate(row_data):
            self.table_widget.setItem(selected_row, i, QTableWidgetItem(data))

    def save_changes(self):
        # Save the changes to the CSV file
        self.data.to_csv("laptop_data.csv", index=False)

    def search_data(self):
        # Search the data for the search text and category
        search_text = self.search_line_edit.text()
        category = self.category_combobox.currentText()
        if category == "All":
            results = self.data.apply(lambda row: row.astype(str).str.contains(search_text, case=False).any(), axis=1)
        else:
            results = self.data[category].astype(str).str.contains(search_text, case=False)
        filtered_data = self.data[results]
        self.table_widget.setRowCount(filtered_data.shape[0])
        for row in range(filtered_data.shape[0]):
            for col in range(filtered_data.shape[1]):
                item = QTableWidgetItem(str(filtered_data.iloc[row, col]))
                self.table_widget.setItem(row, col, item)

    def clear_search(self):
        # Clear the search results and display all the data
        self.search_line_edit.clear()
        self.category_combobox.setCurrentIndex(0)
        self.populate_table_widget()
  
        
# if __name__ == "__main__":
#    app = QApplication([])
#    window = MyWindow()
#    window.show()
#    sys.exit(app.exec_())
