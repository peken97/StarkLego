import matplotlib.pyplot as plt
from math import ceil


class AgentPerformanceTracker():
    def __init__(self):
        self.data = XY_Data()
        self.size_of_data_group_to_be_averaged = 100
        self.plotter = Plotter()
        
    def append(self, x, y):
        self.data.append(x, y)

    def generate_data_condensed(self):
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

    def generate_csv(self, file_name, condensed=True):

        x = None
        y = None
        if condensed:
            x, y = self.generate_data_condensed()
        else:
            x = self.data.x
            y = self.data.y

        f = open(file_name, "w")
        file_data = "Episode #, Reward\n"
        for index in range(x.__len__()):
            file_data += "{},{}\n".format(x[index], y[index])
        f.write(file_data)
        f.close()

    def plot(self):
        x, y = self.generate_data_condensed()

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