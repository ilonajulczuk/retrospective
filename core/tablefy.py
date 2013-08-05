

class TablefyMixin(object):
    @classmethod
    def as_header(cls, number=True):
        basic_header =  " ".join(
            [ "<th>%s</th>" % field for field in cls.public_fields])
        if number:
            return "<th>#</th>" + basic_header
        else:
            return basic_header
    
    def as_table_row(self, number=None):
        row_cells = " ".join([
            "<td>%s</td>" % getattr(self, field)
            for field in getattr(self, "public_fields")])
        if number is not None:
            
            return "<tr><td>%d</td>%s</tr>" % (number, row_cells)
        else:
            return "<tr>%s</tr>" % row_cells