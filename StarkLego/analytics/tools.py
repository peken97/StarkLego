import matplotlib.pyplot as plt
from math import ceil


class AgentPerformanceTracker():
    def __init__(self):
        self.data = XY_Data()
        self.size_of_data_group_to_be_averaged = 100
        self.plotter = Plotter()
        
    def append(self, x, y):
        self.data.append(x, y)

    def generate_data(self):
        length = self.data.length
        spacing = ceil(length/self.size_of_data_group_to_be_averaged)
        x = []
        y = []
        i = 0
        summed_reward = 0
        for total_reward_in_episode in self.data.y:
            i += 1
            summed_reward += total_reward_in_episode
            if i == spacing:
                y.append(summed_reward/i)
                i = 0
                summed_reward = 0
        
        x = self.data.x[spacing-1::spacing]

        return x, y

    def generate_csv(self, file_name):
        x, y = generate_data(self)
        f = open(file_name, "a")
        for index in self.data.length:
            lineToAppend = "{},{}\n".format(x[i], y[i])
            f.write(lineToAppend)
        f.close()
        #create a file that will store the data as a csv

    def plot(self):
        x, y = self.generate_data()

        self.plotter.plot(x, y, 'Episode #', 'Average Cumulative Reward', 'Performance of Agent')

class Plotter():
    def plot(self, x, y, label_x_axis, label_y_axis, label_z_axis):
        plt.scatter(x, y, s=1)
        plt.xlabel(label_x_axis) 
        plt.ylabel(label_y_axis) 
        plt.title(label_z_axis)
        plt.show()

class XY_Data():
    def __init__(self):
        self.x = []
        self.y = []
        self.length = 0
    def append(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.length += 1