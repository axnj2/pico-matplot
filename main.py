from pico_csv_parser import pico_read_csv
from oscilloscope_graphs import draw_trace
import os
import shutil

INPUT_DIRECTORY = "input/"
OUTPUT_DIRECTORY = "output/"


def process_all_csv():
    # check if the output directory exists if so clear it if not create it
    if os.path.isdir(OUTPUT_DIRECTORY):
        shutil.rmtree(OUTPUT_DIRECTORY)
        os.mkdir(OUTPUT_DIRECTORY)
    else:
        os.mkdir(OUTPUT_DIRECTORY)

    # fetch all the files in the input directory
    input_section = os.listdir(INPUT_DIRECTORY)
    for directory in input_section:
        directory = directory + "/"
        if not os.path.isdir(OUTPUT_DIRECTORY + directory):
            os.mkdir(OUTPUT_DIRECTORY + directory)

        input_setting_directory = os.listdir(INPUT_DIRECTORY + directory)
        for setting_folder in input_setting_directory:
            setting_path = setting_folder + "/"
            if not os.path.isdir(OUTPUT_DIRECTORY + directory + setting_path):
                os.mkdir(OUTPUT_DIRECTORY + directory + setting_path)

            input_files = os.listdir(INPUT_DIRECTORY + directory + setting_path)

            if setting_folder == "NOT_DEFINED":

                for file in input_files:
                    current_locale = directory + setting_path
                    # read the file
                    parsed_data = pico_read_csv(INPUT_DIRECTORY + current_locale + file)
                    # plot the data
                    draw_trace(parsed_data, save_path=OUTPUT_DIRECTORY + current_locale + file.replace(".csv", ".png"))

            else:
                settings = setting_folder.split(";") # format : title_title text;x_min_x_max_x;y_min_y_max_y;unit_force unit
                y_lim = [None, None]
                x_lim = [None, None]
                title = ""
                for setting in settings:
                    setting_data = setting.split("_")
                    if setting_data[0] == "title":
                        title = setting_data[1]
                    elif setting_data[0] == "x":
                        x_lim = setting_data[1:]
                        x_lim = list(map(lambda x: float(x.replace(",", ".")), x_lim))
                    elif setting_data[0] == "y":
                        y_lim = setting_data[1:]
                        y_lim = list(map(lambda x: float(x.replace(",", ".")), y_lim))
                    elif setting_data[0] == "unit":
                        force_unit = setting_data[1]
                    else:
                        raise ValueError(f"Unknown setting : {setting_data[0]}  in folder {setting_folder}")

                for file in input_files:
                    current_locale = directory + setting_path
                    # read the file
                    parsed_data = pico_read_csv(INPUT_DIRECTORY + current_locale + file)
                    # plot the data
                    draw_trace(parsed_data, title_text=title,
                               save_path=OUTPUT_DIRECTORY + current_locale + file.replace(".csv", ".png"),
                               min_x=x_lim[0], max_x=x_lim[1], min_y=y_lim[0], max_y=y_lim[1])




if __name__ == "__main__":
    process_all_csv()