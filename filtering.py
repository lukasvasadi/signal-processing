import csv
import math
import statistics


# First order low pass filter
def low_pass_filter(time, data):
    time_diff = []
    for i in range(1, len(time)):
        time_diff.append(time[i] - time[i-1])

    T = statistics.mean(time_diff) # Time interval
    tau = 1e5  # Time constant in milliseconds
    exponent = -2.0 * math.pi * T / tau
    alpha = math.exp(exponent)

    data_filtered = []
    for i in range(len(data)):
        if i == 0:
            data_filtered.append((1-alpha) * data[i])
        else:
            data_filtered.append((1-alpha) * data[i] + alpha * data_filtered[i-1])
    return data_filtered


# First order high pass filter
def high_pass_filter(time, data):
    time_diff = []
    for i in range(1, len(time)):
        time_diff.append(time[i] - time[i-1])

    T = statistics.mean(time_diff) # Time interval
    tau = 1e6 # Time constant in milliseconds
    exponent = -2.0 * math.pi * T / tau
    alpha = math.exp(exponent)

    data_filtered = []
    for i in range(len(data)):
        if i == 0:
            data_filtered.append((1+alpha)/2 * data[i])
        else:
            data_filtered.append((1+alpha)/2 * data[i] - (1+alpha)/2 * data[i-1] + alpha * data_filtered[i-1])
    return data_filtered


# Save data to csv file
def save_data_filtered(path, time, sen1, sen2):
    fieldnames = ["time", "sen1", "sen2"]
    with open(path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(fieldnames)

        for i in range(len(time)):
            csv_writer.writerow([time[i], sen1[i], sen2[i]])


def main():
    # Initialize data set
    time = []
    sen1 = []
    sen2 = []

    file_path = input("File path: ")
    file_path = file_path[1:-1]

    path_data_filtered = file_path[:-4] + '_filtered.csv'

    # Read csv data and store inside list
    with open(file_path, 'r') as data_file:
        csv_reader = csv.reader(data_file, delimiter=',')
        first_row = True
        for row in csv_reader:
            if first_row:
                first_row = False
            else:
                time.append(float(row[0]))
                sen1.append(float(row[1]))
                sen2.append(float(row[2]))
    
    # Filter dataset
    sen1 = low_pass_filter(time, sen1) 
    sen2 = low_pass_filter(time, sen2)

    save_data_filtered(path_data_filtered, time, sen1, sen2)


if __name__ == '__main__':
    main()
    