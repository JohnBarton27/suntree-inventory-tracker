from datetime import datetime

from sit_object import SitObject
from barcode_print_order_mapping import BarcodePrintOrderMapping


class BarcodePrintOrder(SitObject):

    table_name = 'barcode_print_order'

    def __init__(self, db_id: int = None, name: str = None, initiated: datetime = datetime.now()):
        super().__init__(db_id)
        self._name = name
        self._initiated = initiated
        self._items = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, o):
        if not isinstance(o, BarcodePrintOrder):
            return False

        return self.initiated == o.initiated

    def __hash__(self):
        return hash(self._initiated)

    @property
    def name(self):
        if self._name is None:
            self.populate()

        return self._name

    @property
    def initiated(self):
        if self._initiated is None:
            self.populate()

        return self._initiated

    @property
    def initiated_readable(self):
        return self.initiated.strftime('%b %d %Y - %I:%M:%S %p')

    @property
    def items(self):
        if len(self._items) == 0:
            mappings = BarcodePrintOrderMapping.get_for_order(self)

            for mapping in mappings:
                self._items.append(mapping.item)

        return self._items

    @property
    def num_items(self):
        return len(self.items)

    def add_item(self, item):
        if item in self.items:
            # Refuse to add the same item twice
            return

        new_mapping = BarcodePrintOrderMapping(barcode_print_order=self, item=item)
        new_mapping.create()

        self._items.append(item)

    def remove_item(self, item):
        mapping_to_remove = BarcodePrintOrderMapping(barcode_print_order=self, item=item)
        mapping_to_remove.delete()

        self._items.remove(item)

    def _get_create_params_dict(self):
        return {
            'order_name': self._name,
            'initiated': int(self._initiated.timestamp())
        }

    def export_for_printing(self, base_url: str):
        from fpdf import FPDF
        page_width = 4.25
        page_height = 12
        side_margins = 0.2

        font_size = 10
        text_height = font_size / 72

        barcode_height = 0.80
        barcode_width = barcode_height * 3

        # Skip first label because printer margins may cut it off
        initial_y_offset = 0.85

        space_between_barcode = 0.12 + text_height

        barcode_x_offset = (page_width - barcode_width) / 2

        pdf = FPDF(orientation='p', unit='in', format=(page_width, page_height))
        pdf.set_margins(left=side_margins, right=side_margins, top=0)
        pdf.set_font('Arial', size=font_size)

        # Add a page
        pdf.add_page()

        first_of_page = True
        nth_of_page = 0
        all_items = []
        for item in self.items:
            for i in range(0, item.quantity):
                all_items.append(item)

        for i, item in enumerate(all_items):
            if i % 10 == 0 and i != 0:
                # 11th/21st/31st/etc. item, needs new page
                pdf.add_page()
                first_of_page = True

            if i == 0 or first_of_page:
                y_offset = initial_y_offset
                pdf.ln(y_offset)
                nth_of_page = 0
                first_of_page = False
            else:
                y_offset = initial_y_offset + nth_of_page * (space_between_barcode + barcode_height)

            pdf.cell(w=0, border=0, h=text_height, txt=item.description.upper(), align='C', ln=1)
            pdf.ln(barcode_height + space_between_barcode - text_height)

            barcode_url = f'{base_url}/api/items/{item.id}/barcode.png'
            pdf.image(name=barcode_url, h=barcode_height, w=barcode_width, x=barcode_x_offset, y=y_offset + text_height)

            nth_of_page += 1

        # save the pdf with name .pdf
        pdf.output("GFG.pdf")

    @classmethod
    def _get_from_db_result(cls, db_result):
        initiated_ts = int(db_result['initiated'])
        initiated = datetime.fromtimestamp(initiated_ts)
        return BarcodePrintOrder(db_id=db_result['id'], name=db_result['order_name'], initiated=initiated)
