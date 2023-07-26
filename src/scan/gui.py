#!/usr/bin/python3
# -*- coding: utf-8 -*-
import flet as ft

from .scan import SCAN, the_statatus_db
import os
from naruno.lib.perpetualtimer import perpetualTimer


network = None
host = None
port = None

interval_1 = None
interval_2 = None


def scan_page(page: ft.Page):
    global interval_1
    global interval_2
    page.scroll = "AUTO"
    page.theme = ft.Theme(font_family="Poppins")

    page.appbar = ft.AppBar(
        bgcolor="#212529",
        leading=ft.Image(
                src=f"https://docs.naruno.org/assets/images/logo.png",
                width=40,
                height=40,
                fit=ft.ImageFit.FIT_WIDTH,
        ),
        leading_width=40,
        title=ft.Text("Naruno Scan"),
        center_title=False,

    )

    the_block_situations = ft.Row([ft.Text(value="False", style="headlineLarge"), ft.Text(value="Loading", style="headlineLarge"), ft.Text(
        value="False", style="headlineLarge"),], alignment=ft.MainAxisAlignment.CENTER)        # type: ignore

    row = ft.ResponsiveRow(spacing=10, controls=[
        ft.Column(col={"sm": 4}, controls=[
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([ft.Text(value="Connected Nodes", style="headlineMedium")],
                                   alignment=ft.MainAxisAlignment.CENTER),  # type: ignore
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("Host")),
                                    ft.DataColumn(
                                        ft.Text("Port"), numeric=True),
                                ],
                                rows=[
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Loading")),
                                        ft.DataCell(ft.Text("0")),

                                    ],
                                )],
                            ),
                        ],
                        scroll="AUTO",
                    ),
                    padding=10,
                ),
                height=180,
                width=400,
            ),
        ]),


        ft.Column(col={"sm": 4}, controls=[ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([ft.Text(value="Health", style="headlineMedium")],
                               alignment=ft.MainAxisAlignment.CENTER),  # type: ignore
                        ft.Row([ft.Text("Loading", style="headlineSmall",
                               color="#00ff00")], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.Text("Loading", style="headlineSmall",
                               color="#00ff00")], alignment=ft.MainAxisAlignment.CENTER),
                    ]
                ),

                padding=10,
            ),
            height=180,
            width=400,
        ),
        ]),


        ft.Column(col={"sm": 4}, controls=[ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([ft.Text(value="Block", style="headlineMedium")],
                               alignment=ft.MainAxisAlignment.CENTER),  # type: ignore
                        ft.Text(value="Loading", style="headlineSmall"),
                        ft.Text(value="Loading", style="headlineSmall"),
                    ]
                ),

                padding=20,
            ),
            height=180,
            width=400,
        ),

        ]),
    ], alignment=ft.MainAxisAlignment.CENTER)


    tx_row = ft.ResponsiveRow([ft.Card(
        content=ft.Container(
            content=ft.Column(

                [
                    ft.Row([ft.Text(value="Transactions", style="headlineMedium")],
                           alignment=ft.MainAxisAlignment.CENTER),  # type: ignore
                    ft.Row([ft.DataTable(
                            width=1200,
                            columns=[
                                ft.DataColumn(ft.Text("Signature")),
                                ft.DataColumn(ft.Text("Fee")),
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Loading")),
                                        ft.DataCell(ft.Text("Loading")),

                                    ],
                                )],
                            )], scroll="AUTO", alignment=ft.MainAxisAlignment.CENTER)

                ],
                scroll="AUTO",

            ),

            padding=20,
        ),
        width=1220,
        height=540,
    )], alignment=ft.MainAxisAlignment.CENTER)

    def close_bs(e):
            bs.open = False
            bs.update()
    bs = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    [
                        ft.Text("This is sheet's content!"),
                        ft.Row([ft.ElevatedButton("Close bottom sheet", on_click=close_bs)], alignment=ft.MainAxisAlignment.CENTER)
                    ],
                    tight=True,
                ),
                padding=10,
            ),
            open=False,
        )
    page.overlay.append(bs)

    def block_situation_tracker():
        record = the_statatus_db.get("block")
        if record != None:
            first_value = record["round_1"]
            second_value = str(record["sequence_number"])
            third_value = record["round_2"]
            validating_list = record["validating_list"]

            value = 0.1
            if first_value == True:
                value = 0.6
            if third_value == True:
                value = 1
            row.controls[2].controls[0].content.content.controls[1] = ft.Row([ft.Text(
                value=second_value, style="headlineLarge"),], alignment=ft.MainAxisAlignment.CENTER)        # type: ignore
            row.controls[2].controls[0].content.content.controls[2] = ft.ProgressBar(
                value=value, color="#dbff00")



            def show_bs(signature):
                bs.open = True
                the_signature = signature["signature"]
                from_user = signature["fromUser"]
                to_user = signature["toUser"]
                amount = signature["amount"]
                transaction_fee = signature["transaction_fee"]
                bs.content.content.controls = [ft.Text(f"Signature: {the_signature}"),
                                            ft.Text(f"FromUser: {from_user}"),
                                                ft.Text(f"ToUser: {to_user}"),
                                                ft.Text(f"Amount: {amount}"),
                                                ft.Text(f"Fee: {transaction_fee}"),
                                                ft.Row([ft.ElevatedButton("Close", on_click=close_bs)], alignment=ft.MainAxisAlignment.CENTER)
                                            ]
                bs.update()




            
            tx_row.controls[0].content.content.controls[1].controls[0].rows = [
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text(i["signature"]), on_tap=lambda e, i=i: show_bs(i)),
                                            ft.DataCell(ft.Text(i["transaction_fee"])),

                                        ],
                                    ) for i in validating_list]
            


            page.update()

    block_situation_tracker()
    perpetualTimer(interval_1, block_situation_tracker)



    def status_situation_tracker():
        record = the_statatus_db.get("status")
        if record != None:
            working = True if record["status"] == "Working" else False

            if not working:

                row.controls[1].controls[0].content.content.controls[1] = ft.Row([ft.Text("", style="headlineSmall",
                                color="red")], alignment=ft.MainAxisAlignment.CENTER)      # type: ignore
                row.controls[1].controls[0].content.content.controls[2] = ft.Row([ft.Text("Not Working", style="headlineSmall",
                                color="red")], alignment=ft.MainAxisAlignment.CENTER)
            else:
                row.controls[1].controls[0].content.content.controls[1] = ft.Row([ft.ProgressRing(width=50, height=50, stroke_width=5,
                                color="#00ff00")], alignment=ft.MainAxisAlignment.CENTER)    # type: ignore
                row.controls[1].controls[0].content.content.controls[2] = ft.Row([ft.Text("Working", style="headlineSmall",
                                color="#00ff00")], alignment=ft.MainAxisAlignment.CENTER) 

            
            raw_nodes = record["connected_nodes"]
            nodes = []
            for i in raw_nodes:
                nodes.append([i.split(":")[0], i.split(":")[1]])

            row.controls[0].controls[0].content.content.controls[1].rows = [
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text(i[0])),
                                            ft.DataCell(ft.Text(i[1])),

                                        ],
                                    ) for i in nodes]



            page.update()

    status_situation_tracker()
    perpetualTimer(interval_2, status_situation_tracker)


    page.add(row, tx_row,)


def GUI(interval_1_data=1, interval_2_data=100):
    global interval_1
    global interval_2

    interval_1 = interval_1_data
    interval_2 = interval_2_data
    ft.app(target=scan_page, assets_dir=os.path.join(
        os.path.dirname(__file__), "assets"))


def WEB(host_data, port_data, interval_1_data=1, interval_2_data=100):

    global host
    global port
    global interval_1
    global interval_2

    host = host_data
    port = port_data
    interval_1 = interval_1_data
    interval_2 = interval_2_data

    ft.app(target=scan_page, view=ft.AppView.WEB_BROWSER, host=host,
           port=port, assets_dir=os.path.join(os.path.dirname(__file__), "assets"))
