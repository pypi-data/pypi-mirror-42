

import base64

def print_table(data, records_per_page=None, padding=2, headings_justify='center', data_justify='left', border=False, order=()):
    ''' Print data in table format '''

    if not data:
        raise Exception("Empty data set!")

    JUSTIFY = {

        'center': '^',
        'left': '<',
        'right': '>',

    }
    
    headings_justify = headings_justify.lower()
    data_justify = data_justify.lower()

    if headings_justify not in JUSTIFY.keys():
        headings_justify = 'center'
    
    if data_justify not in JUSTIFY.keys():
        data_justify = 'center'

    if order:
        fields = list(order)
        fields += [i for i in data[0].keys() if i not in fields]
        fields = tuple(fields)
    else:
        fields = tuple(data[0].keys())

    '''
            CHECK IF DATA IS NORMAL
        All records need to have the same number of fields and same field names
    
    '''
    for item in data:
        if not all(i in fields for i in item.keys()) or len(item.keys()) != len(fields):
            raise Exception("Fields not consistent")

    '''
            CLEAN THE DATA TYPES
    
        Items with None, bytearrays, or dates need to be converted to str types
    
    '''
    rows =  []
    for item in data:
        sorted_data = []
        
        if order:
            for i in order:
                sorted_data.append(item[i])

            sorted_data += [v for k,v in item.items() if k not in order]
        else:
            sorted_data = list(item.values())

        cleaned_nones = ['' if v is None else v for v in sorted_data]
        # requires, import base64
        cleaned_bytes = [base64.b64encode(v).decode() if type(v) is bytearray else v for v in cleaned_nones]
        cleaned_all = [str(v) for v in cleaned_bytes]

        rows.append(cleaned_all)


    '''
            CALCULATE THE MAX LENGTHS FOR EACH COLUMN
    '''
    # Get the lengths of each field
    lengths = dict(zip(fields, tuple(len(_) for _ in fields)))
 
    # Get the maximum needed length for each column in recordset. e.g the longest str
    for row in data:
        for item in row:
            lengths[item] = max(len(str(row[item])), lengths[item])
    

    '''
            GENERATE ALL THE FORMAT STRINGS FOR PRINTING
    '''
    row_format = ""
    line_format = ""
    clean_row_format = ""
    clean_line_format = ""
    header_format = ""
    clean_header_format = ""

    for field in fields:
        header_format += "{:" + JUSTIFY[headings_justify] + str(lengths[field]) + "}" + " "*padding + "|" + " "*padding
        row_format += "{:" + JUSTIFY[data_justify] + str(lengths[field]) + "}" + " "*padding + "|" + " "*padding
        line_format += "-"*padding + "{:^" + str(lengths[field]) + "}" + "-"*padding + "+"
    
        clean_header_format += "{:" + JUSTIFY[headings_justify] + str(lengths[field]) + "}" + " "*padding + " " + " "*padding
        clean_row_format += "{:" + JUSTIFY[data_justify] + str(lengths[field]) + "}" + " "*padding + " " + " "*padding
        clean_line_format += " "*padding + "{:<" + str(lengths[field]) + "}" + " "*padding + " "
        
    headers = header_format.format(*fields)
    headers = "|" + " "*padding + headers

    clean_headers = clean_header_format.format(*fields)
    clean_headers = " "*padding + clean_headers

    solid_line = "-"*(len(headers)-padding-2)
    solid_line = "|" + solid_line + "|"

    clean_solid_line = " "*(len(headers)-padding-2)
    clean_solid_line = "   " + clean_solid_line + " "
    
    lines = ("-"*lengths[field] for field in fields)
    spacer_line = line_format.format(*lines)
    spacer_line = "|" + spacer_line[:len(spacer_line)-1] + "|"

    lines = ("-"*lengths[field] for field in fields)
    clean_spacer_line = clean_line_format.format(*lines)
    clean_spacer_line = clean_spacer_line[:len(clean_spacer_line)] 
    
    
    if not border:
        
        '''
            PRINT TABLE WITHOUT BORDERS
        '''
        print()
        print(clean_headers)        # e.g.  field1  
        print(clean_spacer_line)    #       ------
        
        for row_num, row in enumerate(rows):
            data_row = clean_row_format.format(*row)
            print(" "*padding + data_row)
            
            if records_per_page:
                if (row_num+1) % records_per_page == 0:
                    r = input("")
        print('\n')  

    else:

        '''
            PRINT TABLE WITH BORDERS
        '''
        print(solid_line)    # e.g. |--------|
        print(headers)       # e.g. | field1 | 
        print(spacer_line)   # e.g. |---+----|
        
        num_rows = len(rows)
        for row_num, row in enumerate(rows):
            data_row = row_format.format(*row)
            print("|" + " "*padding + data_row)

            if (row_num +1) == num_rows:
                print(solid_line)
                
            else:
                print(spacer_line)
            
            if records_per_page:
                if (row_num+1) % records_per_page == 0:
                    r = input("")
        print  

