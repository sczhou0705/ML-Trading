""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""Assess a betting strategy.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  		 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  		 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  		 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  		 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 		  		  		    	 		 		   		 		  
or edited.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  		 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  		 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Shichao Zhou (replace with your name)  		  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: szhou401 (replace with your User ID)  		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 903948749 (replace with your GT ID)  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		  		 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt

  		  	   		  		 		  		  		    	 		 		   		 		  
def author():  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    return "Shichao.Zhou"  # replace tb34 with your Georgia Tech username.
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def gtid():  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    return 903948749 # replace with your GT ID number
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param win_prob: The probability of winning  		  	   		  		 		  		  		    	 		 		   		 		  
    :type win_prob: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: The result of the spin.  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: bool  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    result = False  		  	   		  		 		  		  		    	 		 		   		 		  
    if np.random.random() <= win_prob:  		  	   		  		 		  		  		    	 		 		   		 		  
        result = True  		  	   		  		 		  		  		    	 		 		   		 		  
    return result  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
# def test_code():
#     """
#     Method to test your code
#     """
#     win_prob = 18/38 # set appropriately to the probability of a win
#     np.random.seed(gtid())  # do this only once
#     print(get_spin_result(win_prob))  # test the roulette spin
#     # add your code here to implement the experiments
#
#
# if __name__ == "__main__":
#     test_code()

# Each series of 1000 bets are called an episode
def simulate_simple_bet_strategy(simulate_episodes, win_prob):
    # print("Running strategy for ideal scenario...")
    episode = 1
    each_episode_winnings = [] # Store winnings for each episode
    while episode <= simulate_episodes:
        episode_winnings = 0
        bets = 1
        eposide_winnings_of_each_bet = []
        # Carry over $80 to the next if prev episode reached $80 per requirement
        # Below could be simplified as if episode_winnings < 80: episode_winnings = 0
        # episode starts
        while bets < 1001:
            # bet starts
            if episode_winnings < 80:
                won = False
                bet_amount = 1
                # Keep betting until player won
                while not won:
                    won = get_spin_result(win_prob)
                    if won == True:
                        # bet ends condition 1: player won
                        episode_winnings = episode_winnings + bet_amount
                    else:
                        # bet ends condition 2: player lost
                        episode_winnings = episode_winnings - bet_amount
                        bet_amount *= 2
                    # bet ends events:
                    # 1) increment bet counter;
                    # 2) append current bet's episode winnings to the array;
                    # 3) check if bet counters reach 1000, then continue if < 1000 or break if > 1000
                    bets += 1
                    eposide_winnings_of_each_bet.append(episode_winnings)
                    if bets == 1000:
                        break
            else:
                eposide_winnings_of_each_bet.append(80)
                bets += 1
        # episode ends events: 1) Increment episode counter; 2) Add previous winning records to the result array.
        # print("EP {}: Player reaches ${} in {} bets" .format(episode,episode_winnings,bets))
        episode += 1
        each_episode_winnings.append(eposide_winnings_of_each_bet)
    return each_episode_winnings



# Figure 1
def f1_10_episodes(win_prob):
    plt.figure()
    outcome = simulate_simple_bet_strategy(10,win_prob)
    for i in outcome:
        plt.plot(i)
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel("The number of Bets/Spins",fontsize = 12)
    plt.ylabel("Cumulative winnings",fontsize = 12)
    plt.title("Figure 1: American Roulette Gambling 10 Episodes",fontsize = 16)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.savefig("figure_1.png")
# Figure 2 & 3
def f2_f3_plot(data1, stat_func,title,filename) :
    stats = stat_func(data1, axis=0)
    std_dev = np.std(data1, axis=0)

    plt.figure()
    plt.plot(stats, label=title,color="black",linewidth=2.0)
    plt.plot(stats + std_dev, linestyle='dashed', color='purple', label=f"{title} + 1 std dev")
    plt.plot(stats - std_dev, linestyle='dashed', color='blue', label=f"{title} - 1 std dev")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel("The number of Bets/Spins", fontsize=12)
    plt.ylabel("Cumulative winnings", fontsize=12)
    plt.title(f"{title} of 1000 Gambling Episodes", fontsize=16)
    plt.legend(fontsize =12)
    plt.grid(True)
    plt.savefig(filename)

def save_as_text(data):
    indices =[]
    for spin, row in enumerate(data,1):
        try:
            index = np.where(row == 80)[0][0]
            results = f"{spin}: The first value 80 is found on {index + 1}"
            indices.append(results)
        except IndexError:
            results =f"{spin}: The value 80 is not found"
            indices.append(results)
    with open('p1_results.txt', 'w') as file:
        for ind in indices:
            file.write(ind + "\n")


def simulate_realistic_bet_strategy(simualte_episodes, win_prob):
    # print("Running strategy for realistic scenario...")
    episode = 1
    each_episode_winnings = [] # Store winnings for each episode
    while episode <= simualte_episodes:
        episode_winnings = 0
        bets = 1
        eposide_winnings_of_each_bet = []
        # episode starts
        bankroll = 256
        while bets < 1001:
            if episode_winnings < 80 and episode_winnings > -256:
                # bet starts
                won = False
                bet_amount = 1
                # Keep betting until player won
                while not won:
                    won = get_spin_result(win_prob)
                    # when player's current eposode winnings cannot cover the bet amount, then they can only use the residual amount.
                    bet_amount = min(bet_amount, bankroll)
                    if won == True:
                        # bet ends condition 1: player won
                        episode_winnings = episode_winnings + bet_amount
                        bankroll += bet_amount
                    else:
                        # bet ends condition 2: player lost
                        episode_winnings = episode_winnings - bet_amount
                        bankroll -= bet_amount
                        bet_amount *= 2
                    # bet ends events:
                    # 1) increment bet counter;
                    # 2) append current bet's episode winnings to the array;
                    # 3) check if bet counters reach 1000, then continue if the counter < 1000 or break if the counter > 1000
                    # 4) *New check condition for realistic: if current episode winning <= -256, then player will lose all money in the current episode, then we quit the game.
                    eposide_winnings_of_each_bet.append(episode_winnings)
                    bets += 1
                    if bets == 1000 or bankroll <= 0:
                        break
            elif episode_winnings >= 80:
                eposide_winnings_of_each_bet.append(80)
                bets += 1
            else:
                eposide_winnings_of_each_bet.append(-256)
                bets += 1

        # episode ends events:
        # 1) Increment episode counter;
        # 2) Add previous winning records to the result array.
        # print("EP {}: Player reaches ${} in {} bets" .format(episode,episode_winnings,bets))
        episode += 1
        each_episode_winnings.append(eposide_winnings_of_each_bet)
    return each_episode_winnings

# Figure 4 & 5
def f4_f5_plot(data2, stat_func,title,filename):
    stats = stat_func(data2, axis=0)
    std_dev = np.std(data2, axis=0)

    plt.figure()
    plt.plot(stats, label=title,color="black",linewidth=2.0)
    plt.plot(stats + std_dev, linestyle='dashed', color='purple', label=f"{title} + 1 std dev")
    plt.plot(stats - std_dev, linestyle='dashed', color='blue', label=f"{title} - 1 std dev")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel("The number of Bets/Spins", fontsize=12)
    plt.ylabel("Cumulative winnings", fontsize=12)
    plt.title(f"{title} of Realistic Gambling Episodes", fontsize=16)
    plt.legend(fontsize =12)
    plt.grid(True)
    plt.savefig(filename)


def test_code():
    """
    Method to test your code
    """
    win_prob = 18 / 38  # https://en.wikipedia.org/wiki/Roulette#Rules_of_play_against_a_casino
    np.random.seed(gtid())  # do this only once
    print(get_spin_result(win_prob))  # test the roulette spin
    # add your code here to implement the experiments
    f1_10_episodes(win_prob)
    # # figure 2 & 3
    data1 =np.array(simulate_simple_bet_strategy(1000, win_prob))
    f2_f3_plot(data1, np.mean, "Figure 2: Mean Winnings", "figure_2.png")
    f2_f3_plot(data1, np.median, "Figure 3: Median Winnings", "figure_3.png")
    save_as_text(data1)
    # # figure 4 & 5
    data2 =np.array(simulate_realistic_bet_strategy(1000, win_prob))
    # Count the frequency of 80 and -256 appearances for each episode
    count_80 = sum(1 for row in data2 if 80 in row)
    count_256 = sum(1 for row in data2 if -256 in row)
    # print(count_80)
    # print(count_256)
    f4_f5_plot(data2, np.mean, "Figure 4: Mean Winnings", "figure_4.png")
    f4_f5_plot(data2, np.median, "Figure 5: Median Winnings", "figure_5.png")



if __name__ == "__main__":
    test_code()