import jhtalib as jhta


def INFO(df, price='Close'):
    """
    Print df Information
    """
    print ('{:28} {:>10d}'.format('LEN:', len(df[price])))
    print ('{:28} {:>16.5f}'.format('MEAN:', jhta.MEAN(df, len(df[price]), price)[-1]))
#    print ('{:28} {:>16.5f}'.format('HARMONIC_MEAN:', jhta.HARMONIC_MEAN(df, len(df[price]), price)[-1]))
    print ('{:28} {:>16.5f}'.format('MEDIAN:', jhta.MEDIAN(df, len(df[price]), price)[-1]))
    print ('{:28} {:>16.5f}'.format('MEDIAN_LOW:', jhta.MEDIAN_LOW(df, len(df[price]), price)[-1]))
    print ('{:28} {:>16.5f}'.format('MEDIAN_HIGH:', jhta.MEDIAN_HIGH(df, len(df[price]), price)[-1]))
    print ('{:28} {:>16.5f}'.format('MEDIAN_GROUPED:', jhta.MEDIAN_GROUPED(df, len(df[price]), price)[-1]))
#    print ('{:28} {:>16.5f}'.format('MODE:', jhta.MODE(df, len(df[price]), price)[-1]))
    print ('{:28} {:>16.5f}'.format('PSTDEV:', jhta.PSTDEV(df, len(df[price]), price)[-1]))
    print ('{:28} {:>16.5f}'.format('PVARIANCE:', jhta.PVARIANCE(df, len(df[price]), price)[-1]))
#    print ('{:28} {:>16.5f}'.format('STDEV:', jhta.STDEV(df, len(df[price]), price)[-1]))
#    print ('{:28} {:>16.5f}'.format('VARIANCE:', jhta.VARIANCE(df, len(df[price]), price)[-1]))
    print ('{:28} {:>16.5f}'.format('MIN:', jhta.MIN(df, len(df[price]), price)[-1]))
    print ('{:28} {:>16.5f}'.format('MAX:', jhta.MAX(df, len(df[price]), price)[-1]))
    print ('{:28} {:>16.5f}'.format('SUM:', jhta.SUM(df, len(df[price]), price)[-1]))

def INFO_TRADES(profit_trades_list, loss_trades_list):
    """
    Print Trades Information
    """
    hr = jhta.HR(len(profit_trades_list), (len(profit_trades_list) + len(loss_trades_list)))
    plr = jhta.PLR((sum(profit_trades_list) / len(profit_trades_list)), (sum(loss_trades_list) / len(loss_trades_list)))
    ev = jhta.EV(hr, (sum(profit_trades_list) / len(profit_trades_list)), (sum(loss_trades_list) / len(loss_trades_list)))
    por = jhta.POR(hr, plr)
    print ('{:28} {:>16.5f}'.format('Hit Rate / Win Rate:', hr))
    print ('{:28} {:>16.5f}'.format('Profit/Loss Ratio:', plr))
    print ('{:28} {:>16.5f}'.format('Expected Value:', ev))
    print ('{:28} {:>10d}'.format('Probability of Ruin:', por))

