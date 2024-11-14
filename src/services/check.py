from datetime import datetime


class CheckView:
    def __init__(self, business_name, items, total, payment_method, change, line_width=32):
        self.business_name = business_name
        self.items = items
        self.total = total
        self.payment_method = payment_method
        self.change = change
        self.line_width = line_width

    def format_item(self, quantity, price, name):
        item_line = f"{quantity} x {price:,.2f}"
        item_total = f"{quantity * price:,.2f}"
        name_line = f"{name[:self.line_width]}"
        formatted_line = f"{item_line:<{self.line_width - len(item_total)}}{item_total}"
        return f"{name_line}\n{formatted_line}"

    def generate(self):
        lines = []
        separator = "=" * self.line_width
        lines.append(f"{self.business_name:^{self.line_width}}")
        lines.append(separator)
        for item in self.items:
            item = item.dict()
            lines.append(self.format_item(item["quantity"], item["price"], item["name"]))
            lines.append("-" * self.line_width)
        lines.pop()
        lines.append(separator)
        lines.append(f"{'СУМА':<{self.line_width - len(f'{self.total:,.2f}')}}{self.total:,.2f}")
        lines.append(f"{self.payment_method:<{self.line_width - len(f'{self.total:,.2f}')}}{self.total:,.2f}")
        lines.append(f"{'Решта':<{self.line_width - len(f'{self.change:,.2f}')}}{self.change:,.2f}")
        lines.append(separator)
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        lines.append(f"{current_time:^{self.line_width}}")
        lines.append(f"{'Дякуємо за покупку!':^{self.line_width}}")

        return "\n".join(lines)

