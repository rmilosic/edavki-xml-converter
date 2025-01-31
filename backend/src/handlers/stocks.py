import os
import pandas as pd

from src.handlers import get_parser
from src.xml_builder.stocks import build_stock_xml

from collections import deque
import pandas as pd


def process_stocks(args, config):
    # init queue and fifo  
    fifo_queue = deque()
    fifo = 0
    
    # retrieve arguments
    source = args.source
    year = args.year
    
    # Function to handle buying stocks
    def buy(quantity, price, date, isin):
        nonlocal fifo
        fifo = fifo + quantity
        fifo_queue.append((quantity, price, date, fifo))
        # print("fifo", fifo)

    # Function to handle selling stocks and calculate profit/loss
    def sell(quantity, sale_price, sell_date, isin):
        nonlocal fifo
        sold_qty = quantity
        total_cost = 0
        # total_proceeds is equal to quantity and sale price
        total_proceeds = quantity * sale_price
        # 1% of total proceeds
        total_proceeds_1_perc = 0.01 * total_proceeds
        
        # sell table
        sell_table = pd.DataFrame(columns=["date", "date_sold", "sold_qty", "sold_price", "date_bought", "bought_qty", "bought_price", "fifo", "fifo_sold"])
        
        # while quantity of sold stock is greater than 0
        while quantity > 0:
            # get oldest bought stock
            oldest_stock = fifo_queue.popleft()
            available_qty, buy_price, buy_date, fifo_at_buy = oldest_stock
            
            # add buy record to match the sell record
            sell_table.loc[len(sell_table)] = {
                "date": buy_date,
                "date_sold": pd.NA,
                "sold_qty": pd.NA,
                "sold_price": pd.NA,
                "date_bought": buy_date,
                "bought_qty": round(available_qty, 4),
                "bought_price": round(buy_price, 4),
                "fifo": round(fifo_at_buy, 4),
                "fifo_sold": pd.NA
            }
            
            
            # if quantity is greater than available quantity of oldest stock
            if quantity >= available_qty:
                # cost is equal to available quantity of oldest stock * buy price
                total_cost += available_qty * buy_price
                # decrease remaining qty of sold stock
                quantity -= available_qty
               
                # decrease fifo by available quantity of oldest stock
                fifo = fifo - available_qty
               
                
            # if sold qty is less or equal to available quantity of oldest stock
            else:
                total_cost += quantity * buy_price
                # place the remaining bought qty of oldest stock back to the fifo queue
                fifo_queue.appendleft((available_qty - quantity, buy_price, buy_date, fifo_at_buy))
                
                # decrease fifo by sold quantity
                fifo = fifo - quantity
                
                # # add a sell record
                # sell_table.loc[len(sell_table)] = {
                # "date": sell_date,
                # "date_sold": sell_date,
                # "sold_qty": round(quantity, 4),
                # "sold_price": round(sale_price, 4),
                # "date_bought": pd.NA,
                # "bought_qty": pd.NA,
                # "bought_price": pd.NA,
                # "fifo": round(fifo, 4),
                # "fifo_sold": round(fifo, 4)
                # }
                
                # remaining quantity is 0
                quantity = 0
        
         # add a sell record
        sell_table.loc[len(sell_table)] = {
            "date": sell_date,
            "date_sold": sell_date,
            "sold_qty": round(sold_qty, 4),
            "sold_price": round(sale_price, 4),
            "date_bought": pd.NA,
            "bought_qty": pd.NA,
            "bought_price": pd.NA,
            "fifo": round(fifo, 4),
            "fifo_sold": round(fifo, 4)
        }
           
        # 1% of total cost
        total_cost_1_perc = 0.01 * total_cost
            
                
        # Calculate profit/loss
        profit_or_loss_net = total_proceeds - total_cost
        profit_decreased_by_normed_costs = 0
        
        if profit_or_loss_net > 0:
            # normed costs at 1% sale proceeds and 1% purchase proceeds - cannot exceed tax base
            # Normirani stroški, povezani s pridobitvijo in odsvojitvijo kapitala, se priznajo največ v višini, ki ne sme preseči nižjega od:
            #     1.     seštevka 1% od nabavne vrednosti kapitala in 1% od vrednosti kapitala ob odsvojitvi, ali
            normed_costs = total_cost_1_perc + total_proceeds_1_perc
            #     2.     pozitivne razlike med vrednostjo kapitala ob odsvojitvi in vrednostjo kapitala ob pridobitvi.
            profit_decreased_by_normed_costs = profit_or_loss_net - min(profit_or_loss_net, normed_costs)
        
        # return total_cost, total_proceeds, profit_or_loss_net, sell_table
        return total_cost, total_proceeds, profit_or_loss_net, profit_decreased_by_normed_costs, sell_table
    
    # FIFO queue to hold purchased stocks
    parser = get_parser(args.source)
    
    transactions_df = parser.parse_transactions(args.file_path, args.year)
    
    overall_sales_data = pd.DataFrame(columns=["isin", "date_sold", "sold_qty", "sold_price", "date_bought", "bought_qty", "bought_price", "fifo", "fifo_sold"])

    
    overall_loss = 0
    overall_profit = 0
    overall_profit_decreased_nominal_costs = 0
    
    for isin in transactions_df["isin"].drop_duplicates():
        
        # datum, Product, isin, Count, price, fifo cost, proceeds, profit/loss
        # sales_records = []
        product_data = transactions_df[transactions_df["isin"] == isin]
        product_data = product_data.sort_values("Date", ascending=True, axis=0)
        
        sale_master_table = pd.DataFrame(columns=["date", "isin", "date_sold", "sold_qty", "sold_price", "date_bought", "bought_qty", "bought_price", "fifo", "fifo_sold"])
        overall_isin_profit = 0
        overall_isin_loss = 0
        overall_isin_profit_decreased_nominal_costs = 0
        
        fifo = 0
        
        for index, row in product_data.iterrows():
            
   
            count = row["Count"]
            price = row["Amount"]
            date = row["Date"]
            
            try:
                product = row["Product"]
            except KeyError:
                product = row["isin"]
            
            if source == 'degiro':
                action = "buy" if count > 0 else "sell"
            elif source == 'portu':
                action = "buy" if row["Hodnota"] < 0 else "sell"
            else:
                raise NotImplementedError
            
            if action == 'buy':
                buy(count, price, date, product)
            elif action == 'sell':
                
                    
                total_cost, total_proceeds, profit_or_loss, profit_decreased_by_normed_costs, sell_table = sell(abs(count), price, date, product)
                
                    
                sell_table["isin"] = row["isin"]
                
                if date.year == year:
                    sale_master_table = pd.concat([sale_master_table, sell_table], axis=0, ignore_index=True)
                    
                    if profit_or_loss > 0:
                        overall_profit += profit_or_loss
                        overall_isin_profit += profit_or_loss
                        
                        overall_profit_decreased_nominal_costs += profit_decreased_by_normed_costs
                        overall_isin_profit_decreased_nominal_costs += profit_decreased_by_normed_costs
                        
                    elif profit_or_loss < 0:
                        overall_loss += profit_or_loss
                        overall_isin_loss += profit_or_loss
                    
                    # sales_records.append((row["Date"], product, row["isin"], row["Count"], row["Amount"], total_cost, total_proceeds, profit_or_loss))
                    # print(f"Sold {count} shares of {product}:")
                    # print(f"  FIFO Cost: €{total_cost}")
                    # print(f"  Proceeds: €{total_proceeds}")
        # IMPORTAN: empty fifo_deque
        fifo_queue.clear()
         
        # sale_master_table.sort_values(["fifo_sold", "date"], axis=0, ascending=[False, True], inplace=True)
        sale_master_table.sort_values([ "date_bought", "date", "fifo_sold"], axis=0, ascending=[True, True, False], inplace=True)
        sale_master_table.drop_duplicates(inplace=True, subset=["date_bought", "bought_price", "fifo"])
        overall_sales_data = pd.concat([overall_sales_data, sale_master_table], axis=0, ignore_index=True)

        tax_isin = overall_isin_profit_decreased_nominal_costs * 0.25
        print(f"  ISIN summary: {isin}")
        print(f"  Total Profit: €{overall_isin_profit}")
        print(f"  Total Loss: €{overall_isin_loss}")
        print(f"  Total Profit Decreased by Nominal Costs: €{overall_isin_profit_decreased_nominal_costs}")
        print(f"  Calculated taxes: € {tax_isin} \n\n")
        # fifo_sales = pd.DataFrame(columns=["Datum", "Product", "isin", "Count", "Amount", "fifo cost", "proceeds", "profit/loss"], data=sales_records)
        # fifo_sales.to_csv(f"{source}_fifo_{product}.csv", encoding='utf-8')
        
        # file directory
        # if args.portfolio:
        #     dirpath = os.path.join(os.getcwd(), "output", str(source), "stocks", str(year), args.portfolio)
        # else:
        dirpath = os.path.join(os.getcwd(), "output", str(source), "stocks", str(year))
        
        if len(sale_master_table) > 0:
            
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            sale_master_table.to_csv(os.path.join(dirpath, f"{source}_fifo_detail_{product}.csv"), encoding='utf-8')
        
        if len(overall_sales_data) > 0:
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            overall_sales_data.to_csv(os.path.join(dirpath, f"{source}_overall.csv"), encoding='utf-8')
            
            # Build XML
            xml_data = build_stock_xml(overall_sales_data, args.year, config)

            with open(os.path.join(dirpath, f"degiro_stocks_doh_kdvp_v9_{args.year}.xml"), "w", encoding="utf-8") as file:
                file.write(xml_data)
                
    tax = (overall_profit_decreased_nominal_costs + overall_loss) * 0.25
    print(f"  \n \n Overall summary:")
    print(f"  Total Profit: €{overall_profit}")
    print(f"  Total Loss: €{overall_loss}")
    print(f"  Total Profit Decreased by Nominal Costs: €{overall_profit_decreased_nominal_costs}")
    print(f"  Calculated taxes {tax}")
            
            
            
                
    return transactions_df

