import re
import sys
import os
import keyword
import numpy as np

# Parses fields inside a message block
# Supports scalar types (with _t suffix), defaults, and multi-dimensional arrays
# Extracts default values (e.g. '= 0') when present

def parse_fields(body):
    fields = []
    for line in body.splitlines():
        line = line.strip().rstrip(';')
        if not line or line in ('{', '}'):
            continue

        # split into type token and rest
        parts = re.split(r"\s+", line, maxsplit=1)
        if len(parts) < 2:
            sys.exit(f"Error: cannot parse line: {line}")
        type_token, rest = parts

        # extract dims from type_token and rest
        dims = [int(n) for n in re.findall(r"\[([0-9]+)\]", type_token + rest)]
        # clean base type (strip dims)
        base_type = re.sub(r"\[[0-9]+\]", "", type_token)

        # extract field name and default
        m = re.match(r"(\w+)(?:\s*=\s*([0-9]+))?", rest)
        if not m:
            sys.exit(f"Error: missing field name in: {line}")
        name = m.group(1)
        default = m.group(2)

        # validate name
        if not re.match(r'^[A-Za-z_]\w*$', name) or keyword.iskeyword(name):
            sys.exit(f"Error: invalid field name: {name}")
        if any(f['name'] == name for f in fields):
            sys.exit(f"Error: duplicate field: {name}")

        fields.append({'name': name, 'type': base_type, 'dims': dims, 'default': default})
    return fields

# Map supported types to numpy dtype and struct chars
# Keep _t suffix for numeric types; 'byte' is alias for uint8_t
type_map = {
    'int8_t':    ('np.int8',   'b'),
    'int16_t':   ('np.int16',  'h'),
    'int32_t':   ('np.int32',  'i'),
    'int64_t':   ('np.int64',  'q'),
    'uint8_t':   ('np.uint8',  'B'),
    'uint16_t':  ('np.uint16', 'H'),
    'uint32_t':  ('np.uint32', 'I'),
    'uint64_t':  ('np.uint64', 'Q'),
    'float32_t': ('np.float32','f'),
    'float64_t': ('np.float64','d'),
    'byte':      ('np.uint8',  'B'),
}

# Build little-endian struct format string
# Expand arrays by multiplying dimensions
def build_struct_fmt(fields):
    fmt = '<'
    for f in fields:
        np_typ, ch = type_map.get(f['type'], (None, None))
        if ch is None:
            sys.exit(f"Error: unsupported type: {f['type']}")
        count = 1
        for d in f['dims']:
            count *= d
        fmt += f"{count}{ch}" if count > 1 else ch
    return fmt

# Generate Python: one class per message, header defaulted

def gen_python(msgs, base_name):
    out_py = base_name + '.py'
    with open(out_py, 'w') as py:
        py.write("import struct, numpy as np\n\n")
        for name, fields in msgs:
            cls_name = name[0].upper() + name[1:]
            fmt = build_struct_fmt(fields)
            array_field = next((f for f in fields if f['dims']), None)

            py.write(f"class {cls_name}:\n")
            # __init__ signature excluding header
            params = []
            for f in fields:
                if f['name'] == 'header':
                    continue
                if f['dims']:
                    params.append(f"{f['name']}: np.ndarray")
                else:
                    params.append(f"{f['name']}: {type_map[f['type']][0]}")
            if params:
                sig = ', '.join(params)
                py.write(f"    def __init__(self, {sig}):\n")
            else:
                py.write(f"    def __init__(self):\n")

            # set header to its default
            header_field = next(f for f in fields if f['name']=='header')
            hdr_def = header_field['default'] or '0'
            py.write(f"        self.header = np.uint8({hdr_def})\n")
            # remaining fields
            for f in fields:
                if f['name']=='header':
                    continue
                if f['dims']:
                    dtype = f"np.{f['type']}" if f['type']!='byte' else 'np.uint8'
                    py.write(f"        self.{f['name']} = np.asarray({f['name']}, dtype={dtype})  # shape {f['dims']}\n")
                else:
                    py.write(f"        self.{f['name']} = {type_map[f['type']][0]}({f['name']})\n")
            # pack
            py.write("\n    def pack(self) -> bytes:\n")
            if array_field:
                py.write(f"        flat = self.{array_field['name']}.ravel()\n")
                py.write(f"        return struct.pack('{fmt}', self.header, *flat)\n")
            else:
                vals = ', '.join(f"self.{f['name']}" for f in fields)
                py.write(f"        return struct.pack('{fmt}', {vals})\n")
            # unpack
            py.write(f"\n    @classmethod\n    def unpack(cls, b: bytes) -> '{cls_name}':\n")
            if array_field:
                py.write(f"        allv = struct.unpack('{fmt}', b)\n")
                py.write("        header = allv[0]\n")
                py.write(f"        data = np.array(allv[1:], dtype=np.{array_field['type']})\n")
                py.write(f"        data = data.reshape({array_field['dims']})\n")
                py.write(f"        return cls(data)  # header is constant\n\n")
            else:
                py.write(f"        vals = struct.unpack('{fmt}', b)\n")
                args = ', '.join(f"vals[{i}]" for i,f in enumerate(fields) if f['name']!='header')
                py.write(f"        return cls({args})\n\n")

        # Message dispatch map and decoder
        py.write("\n\n# --- Dispatch table and decoder ---\n")
        py.write("msg_dispatch = {\n")
        for name, fields in msgs:
            header_field = next(f for f in fields if f['name'] == 'header')
            header_val = header_field['default'] or '0'
            cls_name = name[0].upper() + name[1:]
            py.write(f"    {header_val}: {cls_name},\n")
        py.write("}\n\n")

        py.write("def decode_msg(blob: bytes):\n")
        py.write("    header = blob[0]\n")
        py.write("    cls = msg_dispatch.get(header)\n")
        py.write("    if cls is None:\n")
        py.write("        raise ValueError(f'Unknown message header: {header}')\n")
        py.write("    return cls.unpack(blob)\n")

    print(f"Generated Python -> {out_py}")

# Generate C++: one struct per message with header default initializer

def gen_cpp(msgs, base_name):
    out_h = base_name + '.h'
    guard = base_name.upper() + '_H'
    with open(out_h, 'w') as h:
        h.write(f"#ifndef {guard}\n#define {guard}\n\n#include <cstdint>\n\n")
        for name, fields in msgs:
            h.write(f"struct {name} {{\n")
            for f in fields:
                arr = ''.join(f"[{d}]" for d in f['dims'])
                if f['name']=='header':
                    val = f['default'] or '0'
                    h.write(f"    {f['type']} header = {val};\n")
                else:
                    h.write(f"    {f['type']} {f['name']}{arr};\n")
            h.write("};\n\n")
        h.write(f"#endif // {guard}\n")
    print(f"Generated C++ -> {out_h}")

# main entrypoint
if __name__ == '__main__':
    if len(sys.argv)!=2:
        print(f"Usage: {sys.argv[0]} <file.msg>")
        sys.exit(1)

    fname = sys.argv[1]
    base, _ = os.path.splitext(os.path.basename(fname))
    text = open(fname).read()

    msgs = []
    for m in re.finditer(r"message\s+(\w+)\s*\{([\s\S]*?)\}\s*", text):
        msgs.append((m.group(1), parse_fields(m.group(2))))

    if not msgs:
        sys.exit("Error: no messages found in file")

    gen_python(msgs, base)
    gen_cpp(msgs, base)
