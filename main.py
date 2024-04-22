import flet as ft


class Despesas(ft.DataTable):
    def __init__(self):
        super().__init__()

        self.columns = [
            ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Categoria")),
            ft.DataColumn(ft.Text("Valor")),
        ]

class DespesaItem(ft.DataRow):
    def __init__(self, despesa_item):
        super().__init__()

        self.alignment = ft.MainAxisAlignment.SPACE_AROUND
        self.cells = [
            ft.DataCell(ft.Text(despesa_item["date"])),
            ft.DataCell(ft.Text(despesa_item["description"])),
            ft.DataCell(ft.Text(despesa_item["category"])),
            ft.DataCell(ft.Text("R$" + despesa_item["price"])),
        ]

class Modal(ft.AlertDialog):
    despesa_model = {
        "date": ft.TextField(),
        "description": ft.TextField(),
        "category": ft.Dropdown(
            options=[
                ft.dropdown.Option("Mercado"),
                ft.dropdown.Option("Padaria"),
                ft.dropdown.Option("Energia"),
                ft.dropdown.Option("Internet"),
            ]
        ),
        "price": ft.TextField(
            hint_text="",
            prefix_text="R$",
        ),
    }

    new_despesa = {}
    despesa_list = []
    def mostrar_despesa(self, e):
        for i in self.despesa_model:
            self.new_despesa[i] = self.despesa_model[i].value
        self.despesa_list.append(self.new_despesa)

        print("2. ", self.despesa_list)

        self.despesas.rows.append(DespesaItem(despesa_item=self.new_despesa))

        for i in self.despesa_model:
            self.despesa_model[i].value = ""
        self.open = False
        self.page.update()

    def cancelar(self, e):
        for i in self.despesa_model:
            self.despesa_model[i].value = ""
        self.open = False
        self.page.update()

    def __init__(self, despesas):
        super().__init__()
        self.title = ft.Text('Preencha os Campos')
        self.content = ft.Column(
            controls=[
                ft.Text("Data"),
                self.despesa_model["date"],
                ft.Text("Descrição"),
                self.despesa_model["description"],
                ft.Text("Categoria"),
                self.despesa_model["category"],
                ft.Text("Valor"),
                self.despesa_model["price"],
            ]
        )
        self.actions = [
            ft.TextButton(
                "Cancelar",
                on_click=self.cancelar,
                style= ft.ButtonStyle(
                    color=ft.colors.RED_400,
                )
            ),
            ft.TextButton(
                "Salvar",
                on_click = self.mostrar_despesa,
            ),
        ]
        self.despesas = despesas
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN


def main(page: ft.Page):
    page.title = "Finanças"

    despesas = Despesas()
    modal = Modal(despesas=despesas)

    def mostrar_modal(e):
        page.dialog = modal
        modal.open = True
        page.update()

    titulo = ft.Text('Despesas')
    bt_adiciona_despesas = ft.ElevatedButton(
        'Adicione nova Despesa',
        on_click = mostrar_modal
    )

    page.add(
        titulo,
        bt_adiciona_despesas,
        ft.ResponsiveRow(controls=[despesas]),
    )


ft.app(target=main)
