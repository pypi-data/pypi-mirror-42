import math


def table_format_csv(csv_file):
    """
    Receives an arg pointing to a CSV files. Open it and format as a table
    adding "||" and "="
    """

    SPACING = 2
    formatted_text = ""
    with open(csv_file, 'r') as csv_object:

        # First calculate the lengths necessary to build a table
        fields_max_length = None
        line_max_length = 0

        for line in csv_object:

            line_words = split_csv_line(line)

            # Initialize lengths array with 0s
            if not fields_max_length:
                fields_max_length = []
                for i in range(len(line_words)):
                    fields_max_length.append(0)

            # Find the longest word for every field
            j = 0
            for word in line_words:
                if (len(word) + SPACING) > fields_max_length[j]:
                    fields_max_length[j] = len(word) + SPACING
                j += 1

    line_max_length =\
        sum(fields_max_length) + (2 * (len(fields_max_length) - 1))
    separator_line = '=' * line_max_length

    with open(csv_file, 'r') as csv_object:
        # And now let's build the table
        for line in csv_object:
            line_words = split_csv_line(line)

            # Generate a formatted line with filling spaces
            formatted_line = ""
            i = 0
            for word in line_words:
                num_spaces = fields_max_length[i] - len(word)
                formatted_line +=\
                    (math.floor(num_spaces/2) * " ") + word +\
                    (math.ceil(num_spaces/2) * " ") + "||"
                i += 1

            formatted_text +=\
                "||" + formatted_line + "\n" + "||" + separator_line + "||\n"

    return formatted_text


def split_csv_line(line):
    """
    This function splits a single CSV-RFC4180 line and returns a list with the
    values of each of the comma separated fields.
    """

    literal = False
    preceding_quotes = False
    current_field = ""
    fields = []

    for char in list(line):
        if literal:
            if (char == '"') and (preceding_quotes is True):
                current_field += char
                preceding_quotes = False
            elif (char == '"') and (preceding_quotes is False):
                preceding_quotes = True
            elif (char != '"') and (preceding_quotes is True):
                literal = False
                preceding_quotes = False
            elif (char != '"') and (preceding_quotes is False):
                current_field += char

        if not literal:
            if char == '"':
                literal = True
            elif char == ',':
                fields.append(current_field)
                current_field = ""
            else:
                current_field += char

    return fields
