#!/usr/bin/env python

import platform
# Check for the minimal Python version
# Exit if the requirement not satisfied
if float(platform.python_version()[:3]) < float("2.7"):
    print('Python Version on this computer:', platform.python_version()[:3])
    raise RuntimeError('Python version 2.7 or higher required')

import os
import sys
import csv
import re
import argparse

# Running script name
running_script = sys.argv[0]

def get_args():
    myargs = argparse.ArgumentParser(prog=sys.argv[0], \
                                     usage='Example: %(prog)s -t TeamMap.csv -p ProductMaster.csv -s Sales.csv --team-report=TeamReport.csv --product-report=ProductReport.csv', \
                                     description="Reports Generator")

    myargs.add_argument("-t", help="Name of TeamMap CSV File", type=argparse.FileType('r'), nargs=1, \
                        action="store", required=True, default=False)
    myargs.add_argument("-p", help="Name of ProductMaster CSV File", type=argparse.FileType('r'), nargs=1, \
                        action="store",  required=True, default=False)
    myargs.add_argument("-s", help="Name of Sales CSV File", type=argparse.FileType('r'), nargs=1, \
                            action="store", required=True, default=False)
    myargs.add_argument("--team-report", help="Name of TeamReport Output File",  type=argparse.FileType('w'), nargs=1, \
                            action="store", dest='team_report_output', required=True)
    myargs.add_argument("--product-report", help="Name of ProductsReport Output File", type=argparse.FileType('w'), nargs=1, \
                            action="store", dest='product_report_output', required=True)
    args = myargs.parse_args()

    return args

def main():
    # Parse input parameters
    args = get_args()

    # Read Input files
    # First TeamMap file
    if args.t[0].name is not None:
        #print(args.t[0].name)
        TeamMap = {}
        with open(args.t[0].name) as team_map_input:
            #skip the header
            next(team_map_input)
            for line in team_map_input:
                (TeamID, Name) = line.split(',')
                TeamMap[int(TeamID)] = Name.rstrip()
    else:
        print('Oh well ; No args, no file, Should not be here')

    # Read the ProductMaster file
    if args.p[0].name is not None:
        #print(args.t[0].name)
        ProductMasterMap = {}
        with open(args.p[0].name) as product_master_input:
            for line1 in product_master_input:
                (ProductID, NameP, Price, LotSize) = line1.split(',')
                ProductMasterMap[int(ProductID)] = {'name' : NameP, 'price' : Price, 'lotsize' : LotSize.rstrip()}
    else:
        print('Oh well ; No args, no file, Should not be here')

    # Read the Sales Input file
    if args.s[0].name is not None:
        SalesMap = {}
        TeamRevenue = {}
        ProductReport = {}
        ProductID = None
        with open(args.s[0].name) as sales_input:
            for line2 in sales_input:
                ProdID_Rev = 0
                new_gross_revenue = 0
                (SalesID, ProductID, TeamID, Quantity, Discount) = line2.split(',')
                discount = Discount.rstrip()
                ProdID_Rev_Line = float(ProductMasterMap[int(ProductID)]['price']) * int(ProductMasterMap[int(ProductID)]['lotsize'])*int(Quantity)
                DiscountCost = ProdID_Rev_Line * float(discount) / 100
                SalesMap[int(SalesID)] = {'producid' : ProductID, 'teamid' : TeamID, 'quantity' : int(Quantity), 'total_sale' : ProdID_Rev_Line, 'discount' : Discount.rstrip()}
                TeamRevenue[int(TeamID)] = TeamRevenue.get(TeamMap[int(TeamID)],0) + SalesMap[int(SalesID)]['total_sale']
                ProductReport[int(ProductID)] = {'grossrevenue': ProdID_Rev_Line, 'totalunits': Quantity, 'discountcost': DiscountCost}

    else:
        print('Oh well ; No args, no file, Should not be here')
  

    #########################
    # Generate Reports
    ##########################
    

    #Generate Team Report
    if args.team_report_output[0].name is not None:
        team_rpt = open(args.team_report_output[0].name, "w")
        team_rpt.write("Team, Gross Revenue")
        team_rpt.write('\n')

        for key, val in TeamRevenue.items():
            team_rpt.write("%s, %s" % (TeamMap[key], val))
            team_rpt.write('\n')

        team_rpt.close()

    #Generate Product Report
    if args.product_report_output[0].name is not None:
        product_rpt = open(args.product_report_output[0].name, "w")
        product_rpt.write("Name, GrossRevenue, TotalUnits, DiscountCost")
        product_rpt.write('\n')

        for key, value in sorted(ProductReport.items(), key=lambda item: item[1]):

            product_rpt.write(str(ProductMasterMap[key]['name']))
            product_rpt.write(", ")
            product_rpt.write(str(ProductReport[key]['grossrevenue']))
            product_rpt.write(", ")
            product_rpt.write(str(ProductReport[key]['totalunits']))
            product_rpt.write(", ")
            product_rpt.write(str(ProductReport[key]['discountcost']))

            product_rpt.write('\n')

        product_rpt.close()

if __name__ == "__main__":
    main()

