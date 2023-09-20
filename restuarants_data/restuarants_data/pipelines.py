import csv
from .items import RestaurantCategoryItem

class CustomCsvExportPipeline:
    def open_spider(self, spider):
        self.csv_file = open('selenium/deliverooptwt.csv', 'a', newline='')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=RestaurantCategoryItem.fields.keys())
        # Write the header only if the file is empty
        if self.csv_file.tell() == 0:
            self.csv_writer.writeheader()

    def close_spider(self, spider):
        self.csv_file.close()

    def process_item(self, item, spider):
        self.csv_writer.writerow(item)
        return item
