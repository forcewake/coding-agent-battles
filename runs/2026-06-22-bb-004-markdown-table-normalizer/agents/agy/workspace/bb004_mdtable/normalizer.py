import re

def split_by_pipes(line: str) -> list[str]:
    cells = []
    current = []
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        if c == '\\':
            if i + 1 < n:
                current.append(line[i:i+2])
                i += 2
                continue
            else:
                current.append(c)
                i += 1
        elif c == '|':
            cells.append("".join(current))
            current = []
            i += 1
        else:
            current.append(c)
            i += 1
    cells.append("".join(current))
    return cells

def get_row_cells(line: str) -> list[str]:
    cells = split_by_pipes(line)
    line_stripped = line.strip()
    
    start_idx = 0
    if line_stripped.startswith('|'):
        start_idx = 1
        
    ends_with_pipe = False
    if line_stripped.endswith('|'):
        # Check if the last pipe is escaped
        backslash_count = 0
        idx = len(line_stripped) - 2
        while idx >= 0 and line_stripped[idx] == '\\':
            backslash_count += 1
            idx -= 1
        if backslash_count % 2 == 0:
            ends_with_pipe = True
            
    end_idx = len(cells) - 1 if ends_with_pipe else len(cells)
    
    return [c.strip() for c in cells[start_idx:end_idx]]

def is_separator_row(line: str) -> bool:
    line_stripped = line.strip()
    if not line_stripped or '|' not in line_stripped:
        return False
    cells = split_by_pipes(line)
    if len(cells) < 2:
        return False
    
    start_idx = 1 if line_stripped.startswith('|') else 0
    
    ends_with_pipe = False
    if line_stripped.endswith('|'):
        backslash_count = 0
        idx = len(line_stripped) - 2
        while idx >= 0 and line_stripped[idx] == '\\':
            backslash_count += 1
            idx -= 1
        if backslash_count % 2 == 0:
            ends_with_pipe = True
            
    end_idx = len(cells) - 1 if ends_with_pipe else len(cells)
    
    if start_idx >= end_idx:
        return False
        
    delim_re = re.compile(r'^:?-+:?$')
    for i in range(start_idx, end_idx):
        cell_val = cells[i].strip()
        if not delim_re.match(cell_val):
            return False
    return True

def parse_code_blocks(lines: list[str]) -> list[bool]:
    in_code_block = False
    fence_char = None
    fence_len = 0
    is_code = []
    for line in lines:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(' '))
        is_fence = False
        if indent <= 3:
            if stripped.startswith('```') or stripped.startswith('~~~'):
                is_fence = True
                char = stripped[0]
                length = 0
                for c in stripped:
                    if c == char:
                        length += 1
                    else:
                        break
        
        if is_fence:
            if not in_code_block:
                in_code_block = True
                fence_char = char
                fence_len = length
                is_code.append(True)
            else:
                if char == fence_char and length >= fence_len:
                    in_code_block = False
                    is_code.append(True)
                else:
                    is_code.append(True)
        else:
            is_code.append(in_code_block)
    return is_code

def format_table(table_lines: list[str]) -> list[str]:
    if not table_lines:
        return []
    # Extract indentation of the first line (header)
    first_line = table_lines[0]
    indent_len = len(first_line) - len(first_line.lstrip(' '))
    indent = first_line[:indent_len]
    
    # Extract C (number of columns in the separator row)
    # The separator row is at index 1
    sep_cells = get_row_cells(table_lines[1])
    C = len(sep_cells)
    
    # Get adjusted cells for all rows
    adjusted_rows = []
    for line in table_lines:
        row_cells = get_row_cells(line)
        if len(row_cells) < C:
            row_cells += [""] * (C - len(row_cells))
        elif len(row_cells) > C:
            row_cells = row_cells[:C]
        adjusted_rows.append(row_cells)
        
    # Normalize separator row (at index 1)
    adjusted_rows[1] = ["---"] * C
    
    # Calculate column widths
    # Note: each column must be at least width 3 (since separator is "---")
    col_widths = []
    for j in range(C):
        max_w = max(max(len(row[j]) for row in adjusted_rows), 3)
        col_widths.append(max_w)
        
    # Format each row
    formatted_lines = []
    for row in adjusted_rows:
        formatted_cells = []
        for j in range(C):
            cell_val = row[j]
            w = col_widths[j]
            padded = cell_val + " " * (w - len(cell_val))
            formatted_cells.append(f" {padded} ")
        row_str = indent + "|" + "|".join(formatted_cells) + "|"
        formatted_lines.append(row_str)
        
    return formatted_lines

def normalize_markdown_tables(markdown: str) -> str:
    if not markdown:
        return markdown
        
    has_carriage_return = "\r\n" in markdown
    # Split by '\n', strip '\r' from each line to process cleanly
    lines = [line.replace('\r', '') for line in markdown.split('\n')]
    
    is_code = parse_code_blocks(lines)
    
    tables = []
    n = len(lines)
    i = 0
    while i < n - 1:
        if is_code[i] or is_code[i+1]:
            i += 1
            continue
            
        # Check if table starts at i
        # We require at least one unescaped pipe in the header, and the next line is a separator row.
        if ('|' in lines[i]) and is_separator_row(lines[i+1]):
            # Start of a table! Let's consume all consecutive lines with pipes
            j = i + 2
            while j < n and not is_code[j] and '|' in lines[j]:
                j += 1
            tables.append((i, j))
            i = j
        else:
            i += 1
            
    # Reconstruct the document
    result = []
    last_idx = 0
    for start, end in tables:
        result.extend(lines[last_idx:start])
        formatted = format_table(lines[start:end])
        result.extend(formatted)
        last_idx = end
    result.extend(lines[last_idx:])
    
    join_char = "\r\n" if has_carriage_return else "\n"
    return join_char.join(result)
