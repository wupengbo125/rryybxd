def weekly_adjustment(context):
    if g.no_trading_today_signal == False:
        # 获取应买入列表
        rank_list, score_df = get_rank(g.etf_pool)
        if rank_list[0] != '399101.XSHE':
            log.info("第一名不是中小盘，清仓处理")
            for stock in context.portfolio.positions.keys():
                order_target_value(stock, 0)
                # 检查是否成功卖出
                if stock not in context.portfolio.positions:
                    log.info(f"10:00动量止损了，成功清仓股票：{stock}")
                else:
                    log.info(f"10:00动量止损了，今天买入的股票：{stock}，下次止损卖出")
            return
        g.not_buy_again = []
        g.target_list = get_stock_list(context)
        target_list = filter_not_buy_again(g.target_list)
        target_list = filter_paused_stock(target_list)
        target_list = filter_limitup_stock(context, target_list)
        target_list = filter_limitdown_stock(context, target_list)
        target_list = filter_highprice_stock(context, target_list)
        target_list = target_list[:g.stock_num]
        log.info(str(target_list))
        log.info("10:00最终筛选后的应该买入股票列表:")
        for stock in target_list:
            log.info(stock)

        # print(day_of_week)
        # print(type(day_of_week))
        # 调仓卖出
        for stock in g.hold_list:
            if (stock not in target_list) and (stock not in g.yesterday_HL_list):
                log.info("卖出[%s]" % (stock))
                position = context.portfolio.positions[stock]
                close_position(position)
            else:
                log.info("已持有[%s]" % (stock))
        # 调仓买入
        buy_security(context, target_list)
        # 记录已买入股票
        for position in list(context.portfolio.positions.values()):
            stock = position.security
            g.not_buy_again.append(stock)